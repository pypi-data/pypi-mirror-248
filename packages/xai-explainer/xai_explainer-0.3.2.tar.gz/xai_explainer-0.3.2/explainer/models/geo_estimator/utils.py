from argparse import Namespace
from collections import OrderedDict
from pathlib import Path
from typing import List, Union

import numpy as np
import pandas as pd
import pytorch_lightning as pl
import s2sphere as s2
import torch
from torch.hub import get_dir, load_state_dict_from_url
import torchvision

from .._api import get_model_dir


def model_loader():
    URL = "https://tu-dortmund.sciebo.de/s/3VU0lpi3mqt5JCp/download"
    DIR = "./explainer/models/geo_estimator/resources/"
    FILE = "epoch=014-val_loss=18.4833.ckpt"
    MODEL_DIR = get_model_dir()
    if MODEL_DIR is None:
        MODEL_DIR = get_dir()
    load_state_dict_from_url(
        url=URL,
        model_dir=MODEL_DIR,
        file_name=FILE,
        map_location="cpu",
    )
    model = MultiPartitioningClassifier.load_from_checkpoint(
        checkpoint_path=f"{MODEL_DIR}/{FILE}",
        hparams_file=f"{DIR}/hparams.yaml",
        map_location=None,
    )
    return model


class MultiPartitioningClassifier(pl.LightningModule):
    def __init__(self, hparams: Namespace):
        super().__init__()
        self.save_hyperparameters(hparams)

        self.partitionings, self.hierarchy = self.__init_partitionings()
        self.model, self.classifier = self.__build_model()

    def __init_partitionings(self):
        partitionings = []
        for shortname, path in zip(
            self.hparams.partitionings["shortnames"],
            self.hparams.partitionings["files"],
        ):
            partitionings.append(Partitioning(Path(path), shortname, skiprows=2))

        if len(self.hparams.partitionings["files"]) == 1:
            return partitionings, None

        return partitionings, Hierarchy(partitionings)

    def __build_model(self):
        model, nfeatures = build_base_model(self.hparams.arch)

        classifier = torch.nn.ModuleList(
            [
                torch.nn.Linear(nfeatures, len(self.partitionings[i]))
                for i in range(len(self.partitionings))
            ]
        )

        if self.hparams.weights:
            model, classifier = load_weights_if_available(
                model, classifier, self.hparams.weights
            )

        return model, classifier

    def forward(self, x):
        fv = self.model(x)
        yhats = [self.classifier[i](fv) for i in range(len(self.partitionings))]
        return yhats


class Partitioning:
    def __init__(
        self,
        csv_file: Path,
        shortname=None,
        skiprows=None,
        index_col="class_label",
        col_class_label="hex_id",
        col_latitute="latitude_mean",
        col_longitude="longitude_mean",
    ):
        """
        Required information in CSV:
            - class_indexes from 0 to n
            - respective class labels i.e. hexid
            - latitude and longitude
        """
        self._df = pd.read_csv(csv_file, index_col=index_col, skiprows=skiprows)
        self._df = self._df.sort_index()

        self._nclasses = len(self._df.index)
        self._col_class_label = col_class_label
        self._col_latitude = col_latitute
        self._col_longitude = col_longitude

        # map class label (hexid) to index
        self._label2index = dict(
            zip(self._df[self._col_class_label].tolist(), list(self._df.index))
        )

        self.name = csv_file.stem  # filename without extension
        if shortname:
            self.shortname = shortname
        else:
            self.shortname = self.name

    def __len__(self):
        return self._nclasses

    def __repr__(self):
        return f"{self.name} short: {self.shortname} n: {self._nclasses}"

    def get_class_label(self, idx):
        return self._df.iloc[idx][self._col_class_label]

    def get_lat_lng(self, idx):
        x = self._df.iloc[idx]
        return float(x[self._col_latitude]), float(x[self._col_longitude])

    def contains(self, class_label):
        if class_label in self._label2index:
            return True
        return False

    def label2index(self, class_label):
        try:
            return self._label2index[class_label]
        except KeyError:
            raise KeyError(f"unkown label {class_label} in {self}")


class Hierarchy:
    def __init__(self, partitionings: List[Partitioning]):
        """
        Provide a matrix of class indices where each class of the finest partitioning will be assigned
        to the next coarser scales.

        Resulting index matrix M has shape: max(classes) * |partitionings| and is ordered from coarse to fine
        """
        self.partitionings = partitionings

        self.M = self.__build_hierarchy()

    def __build_hierarchy(self):
        def _hextobin(hexval):
            thelen = len(hexval) * 4
            binval = bin(int(hexval, 16))[2:]
            while (len(binval)) < thelen:
                binval = "0" + binval

            binval = binval.rstrip("0")
            return binval

        def _create_cell(lat, lng, level):
            p1 = s2.LatLng.from_degrees(lat, lng)
            cell = s2.Cell.from_lat_lng(p1)
            cell_parent = cell.id().parent(level)
            hexid = cell_parent.to_token()
            return hexid

        cell_hierarchy = []

        finest_partitioning = self.partitionings[-1]
        if len(self.partitionings) > 1:
            # loop through finest partitioning
            for c in range(len(finest_partitioning)):
                cell_bin = _hextobin(self.partitionings[-1].get_class_label(c))
                level = int(len(cell_bin[3:-1]) / 2)
                parents = []

                # get parent cells
                for lvl in reversed(range(2, level + 1)):
                    lat, lng = finest_partitioning.get_lat_lng(c)
                    hexid_parent = _create_cell(lat, lng, lvl)
                    # to coarsest partitioning
                    for p in reversed(range(len(self.partitionings))):
                        if self.partitionings[p].contains(hexid_parent):
                            parents.append(
                                self.partitionings[p].label2index(hexid_parent)
                            )

                    if len(parents) == len(self.partitionings):
                        break

                cell_hierarchy.append(parents[::-1])
        M = np.array(cell_hierarchy, dtype=np.int32)
        assert max([len(p) for p in self.partitionings]) == M.shape[0]
        assert len(self.partitionings) == M.shape[1]
        return M


def build_base_model(arch: str):
    # from torchvision.models.resnet import ResNet50_Weights
    # model = torchvision.models.__dict__[arch](weights=ResNet50_Weights.DEFAULT)

    model = torchvision.models.__dict__[arch]()

    # get input dimension before classification layer
    if arch in ["mobilenet_v2"]:
        nfeatures = model.classifier[-1].in_features
        model = torch.nn.Sequential(*list(model.children())[:-1])
    elif arch in ["densenet121", "densenet161", "densenet169"]:
        nfeatures = model.classifier.in_features
        model = torch.nn.Sequential(*list(model.children())[:-1])
    elif "resne" in arch:
        # usually all ResNet variants
        nfeatures = model.fc.in_features
        model = torch.nn.Sequential(*list(model.children())[:-2])
    else:
        raise NotImplementedError

    model.avgpool = torch.nn.AdaptiveAvgPool2d(1)
    model.flatten = torch.nn.Flatten(start_dim=1)
    return model, nfeatures


def load_weights_if_available(
    model: torch.nn.Module, classifier: torch.nn.Module, weights_path: Union[str, Path]
):
    checkpoint = torch.load(weights_path, map_location=lambda storage, loc: storage)

    state_dict_features = OrderedDict()
    state_dict_classifier = OrderedDict()
    for k, w in checkpoint["state_dict"].items():
        if k.startswith("model"):
            state_dict_features[k.replace("model.", "")] = w
        elif k.startswith("classifier"):
            state_dict_classifier[k.replace("classifier.", "")] = w
    model.load_state_dict(state_dict_features, strict=True)
    return model, classifier

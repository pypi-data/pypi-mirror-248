from functools import lru_cache
from typing import List

from PIL import Image
from geopy.exc import GeocoderUnavailable
from geopy.geocoders import Nominatim
from torchvision import transforms

from explainer.datasets.base import ClassificationDataset

from .._api import register_dataset

__all__ = ["Im2GPS"]


@register_dataset
class Im2GPS(ClassificationDataset):
    @staticmethod
    def transform(img: Image):
        size = (224, 224)
        return transforms.Compose(
            [
                transforms.Resize(size),
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ]
        )(img)

    @staticmethod
    def classes() -> List[str]:
        classes = list(
            map(
                list,
                zip(*[partitioning().get_lat_lng(c) for c in range(12893)]),
            )
        )
        return list(map(list, zip(*classes)))

    def get_place_from_coords(lat, lng):
        geolocator = Nominatim(user_agent="xai")
        try:
            location = geolocator.reverse([lat, lng], exactly_one=True, language="en")
            address = location.raw["address"]
            city = address.get("city", "Unknown")
            country = address.get("country", "Unknown")
        except GeocoderUnavailable:
            city = "NO CONNECTION"
            country = "NO CONNECTION"

        return city, country


from pathlib import Path


@lru_cache(maxsize=1)
def partitioning():
    file_path = Path(__file__).parent / "cells_50_1000.csv"
    return Partitioning(file_path, "hierachical", skiprows=2)


import pandas as pd


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

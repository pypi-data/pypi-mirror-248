from typing import List

import torch

from explainer.datasets import Im2GPS

from .._api import ModelType, register_model
from ..base import LIME, LRP, Cam
from .utils import model_loader

__all__ = [
    "GeoEstimator",
]


class GeoEstimator(Cam, LRP, LIME):
    def __init__(self, estimator, **kwargs):
        # super().__init__(output_handle = self._geo_guessr_output_handling, **kwargs)
        super().__init__(
            output_handle=lambda x: [torch.argmax(x, dim=1).item()], **kwargs
        )
        self.pretrained = estimator

    def forward(self, x):
        # x = torch.stack(transforms.FiveCrop((224, 224))(x[0]))
        out = self.pretrained.forward(x)
        return self._geo_guessr_output_handling(out)

    def _cam_target_layers(self):
        for name, layer in self.pretrained.model.named_modules():
            if name == "7.2":
                return [layer]

    def _geo_guessr_output_handling(self, out: List[torch.Tensor]) -> List[int]:

        yhats = [torch.nn.functional.softmax(yhat, dim=1) for yhat in out]
        yhats = [torch.reshape(yhat, (1, 1, *list(yhat.shape[1:]))) for yhat in yhats]

        yhats = [torch.max(yhat, dim=1)[0] for yhat in yhats]

        hierarchy_preds = None
        if self.pretrained.hierarchy is not None:
            hierarchy_logits = torch.stack(
                [
                    yhat[:, self.pretrained.hierarchy.M[:, i]]
                    for i, yhat in enumerate(yhats)
                ],
                dim=-1,
            )
            hierarchy_preds = torch.prod(hierarchy_logits, dim=-1)

            # hierarchy_preds = [torch.argmax(hierarchy_preds, dim=1).item()]
        return hierarchy_preds


@register_model(
    model_type=ModelType.OBJECT_MODEL,
    dataset=Im2GPS,
    config={
        "num_classes": Im2GPS.num_classes(),
        "input_transform": Im2GPS.transform,
    },
)
def geo_estimator(**kwargs):
    estimator = model_loader()
    return GeoEstimator(estimator, **kwargs)

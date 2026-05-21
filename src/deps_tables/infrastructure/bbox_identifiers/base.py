from typing import Dict, List

import cv2
import numpy as np
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.engine import DefaultPredictor

from deps_tables.domain.entities import BoundingBoxEntity
from deps_tables.domain.interfaces import IBBoxIdentifier


class DetectronBasedIdentifier(IBBoxIdentifier):
    SCORE_THRESH_TEST = 0.5
    DETECTOR_MODEL_ZOO_CONFIG = "COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"

    def __init__(self, path_to_weights: str, enable_gpu: bool = False):
        self.cfg = get_cfg()
        self.cfg.MODEL.DEVICE = "cuda" if enable_gpu else "cpu"
        self.cfg.merge_from_file(model_zoo.get_config_file(self.DETECTOR_MODEL_ZOO_CONFIG))
        self.cfg.MODEL.WEIGHTS = path_to_weights
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = self.SCORE_THRESH_TEST
        self.cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
        self.predictor = DefaultPredictor(self.cfg)

    def _identify_borders(self, img: np.ndarray, *, transform: bool = True) -> List[BoundingBoxEntity]:
        params = self._predict(img, transform)
        instances = params["instances"]
        coords = instances.pred_boxes.tensor.tolist()
        scores = instances.scores.tolist()
        return [BoundingBoxEntity.from_tuple(bbox) for bbox in zip(coords, scores)]

    def _predict(self, img: np.ndarray, transform: bool = True) -> Dict:
        img = self._convert_img_to_three_channels(img)
        dilate_img = self._dilate_transform(img) if transform else img
        return self.predictor(dilate_img)

    @staticmethod
    def _dilate_transform(img: np.ndarray) -> np.ndarray:
        kernel = np.ones((2, 2), np.uint8)
        _, mask = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY_INV)  # noqa: WPS432
        dst = cv2.dilate(mask, kernel, iterations=1)
        return cv2.bitwise_not(dst)

    @staticmethod
    def _convert_img_to_three_channels(img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

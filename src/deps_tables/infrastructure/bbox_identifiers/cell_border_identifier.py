from typing import List, Tuple, Union

import cv2
import numpy as np

from deps_tables.domain.entities import BoundingBoxEntity
from deps_tables.domain.interfaces import IBBoxIdentifier


class CellBorderIdentifier(IBBoxIdentifier):
    # image scaling for converting from uint8 to float
    SCALEFACTOR = 1 / 255.0
    # net's input blob's size
    BLOB_SIZE = 608, 608
    # a threshold used to filted boxes by confidence
    DETECTION_THRESHOLD = 0
    # same as detection threshold, but used in nms
    # set to 0, since it's a little faster to filter boxes with 'if'
    SCORE_THRESHOLD = 0
    # threshold used in non-maximun-supression (nms)
    # filters boxes by Intersection over Union (IoU) with other boxes
    NMS_THRESHOLD = 0.25

    def __init__(self, path_to_cfg: str, path_to_weights: str, enable_gpu: bool = False):
        self._net = self._init_net(path_to_cfg, path_to_weights, enable_gpu)
        self._layer_names = self._get_layer_names()

    def identify_borders(self, img: np.ndarray) -> List[BoundingBoxEntity]:
        bboxes = self._predict(img)
        return [BoundingBoxEntity.from_tuple(bbox) for bbox in self._apply_nms(bboxes)]

    @staticmethod
    def _init_net(path_to_cfg: str, path_to_weights: str, enable_gpu: bool) -> cv2.dnn_Net:
        net = cv2.dnn.readNetFromDarknet(path_to_cfg, path_to_weights)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA if enable_gpu else cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA if enable_gpu else cv2.dnn.DNN_TARGET_CPU)
        return net

    def _get_layer_names(self) -> List[str]:
        layer_names = self._net.getLayerNames()
        return [layer_names[i - 1] for i in self._net.getUnconnectedOutLayers()]

    def _predict(self, img: np.ndarray) -> Tuple[List, List]:  # noqa: WPS210
        outputs = self._forward(img)

        bboxes: List[Tuple] = []
        confidences: List[float] = []
        h, w = img.shape[:2]

        for out in outputs:
            for detection in out:
                scores = detection[5:]
                confidence = scores[np.argmax(scores)]
                if confidence > self.DETECTION_THRESHOLD:
                    box = detection[:4] * np.array([w, h, w, h])
                    center_x, center_y, width, height = box.astype(int)

                    x = int(center_x - (width / 2))
                    y = int(center_y - (height / 2))

                    bboxes.append((x, y, int(width), int(height)))
                    confidences.append(float(confidence))

        return bboxes, confidences

    def _forward(self, img: np.ndarray) -> List[np.ndarray]:
        blob = cv2.dnn.blobFromImage(
            self._convert_img_to_three_channels(img),
            self.SCALEFACTOR,
            self.BLOB_SIZE,
        )
        self._net.setInput(blob)
        return self._net.forward(self._layer_names)

    def _apply_nms(self, bboxes: Tuple[List, List]) -> List[Tuple[Tuple[int, ...], float]]:  # noqa: WPS234
        boxes, scores = bboxes
        indices: Union[np.ndarray, Tuple] = cv2.dnn.NMSBoxes(boxes, scores, self.SCORE_THRESHOLD, self.NMS_THRESHOLD)
        if len(indices) > 0:  # noqa: WPS507
            return [(self._get_coords(boxes[i]), scores[i]) for i in indices.flatten()]  # type: ignore
        return []

    @staticmethod
    def _convert_img_to_three_channels(img: np.ndarray) -> np.ndarray:
        return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    @staticmethod
    def _get_coords(bbox: Tuple[int, ...]) -> Tuple[int, ...]:
        # TODO: refactor this!!!!
        x, y, width, height = bbox
        return x, y, x + width, y + height

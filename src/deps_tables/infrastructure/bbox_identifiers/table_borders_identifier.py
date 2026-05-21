from typing import List

import numpy as np
import torch

from deps_tables.domain.entities import BoundingBoxEntity
from deps_tables.infrastructure.bbox_identifiers.base import DetectronBasedIdentifier

TABLE_EXISTANCE_THRESHOLD = 0.55


class TableBorderIdentifier(DetectronBasedIdentifier):
    def is_table_on_image(self, img: np.ndarray) -> bool:
        image_parameters = self._predict(img)
        return bool(torch.any(image_parameters["instances"].scores > TABLE_EXISTANCE_THRESHOLD))

    def identify_borders(self, img: np.ndarray) -> List[BoundingBoxEntity]:
        return self._identify_borders(img)

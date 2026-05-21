from typing import List

import numpy as np

from deps_tables.domain.entities import BoundingBoxEntity
from deps_tables.infrastructure.bbox_identifiers.base import DetectronBasedIdentifier


class ColumnBorderIdentifier(DetectronBasedIdentifier):
    SCORE_THRESH_TEST = 0.6

    def identify_borders(self, img: np.ndarray) -> List[BoundingBoxEntity]:
        return self._identify_borders(img, transform=False)

from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from deps_tables.domain.entities.geom import Shape
from deps_tables.domain.entities.ocr import TextLineEntity
from deps_tables.extras.ocr import TextLineModel


@dataclass
class ImageMetadataEntity:
    textlines: Optional[List[TextLineEntity]] = None
    text_line_models: Optional[List[TextLineModel]] = None
    source_id: Optional[str] = None


@dataclass
class ImageEntity:
    image: np.ndarray
    blob_path: Optional[str] = None
    meta: Optional[ImageMetadataEntity] = None

    @property
    def shape(self) -> Shape[int]:
        return Shape(
            height=self.image.shape[0],
            width=self.image.shape[1],
        )

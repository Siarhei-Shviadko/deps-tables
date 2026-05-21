from abc import ABC, abstractmethod
from operator import itemgetter
from typing import Any, Dict, List, Optional

import numpy as np

from deps_tables.domain.constants import DEFAULT_LANGUAGE
from deps_tables.domain.entities import (
    BoundingBoxEntity,
    RectangleEntity,
    TableEntity,
    TextLineEntity,
)
from deps_tables.domain.entities.image import ImageEntity


class ITableAdapter(ABC):
    @classmethod
    @abstractmethod
    def convert_to_domain_table(cls, document: Any, source_id: Optional[str] = None) -> List[TableEntity]:
        pass

    @classmethod
    def coords_to_relative(cls, coords: List[float], start: float, size: float) -> List[float]:
        return [(coord - start) / size for coord in coords]

    @classmethod
    def convert_idx2coord_to_coords(cls, cell2coord: Dict[int, float]) -> List[float]:
        cells_coords = []
        curr_idx = 0
        for cell_idx, coord in sorted(cell2coord.items(), key=itemgetter(0)):
            while curr_idx < cell_idx:
                cells_coords.append(coord)
                curr_idx += 1
            cells_coords.append(coord)
            curr_idx += 1
        return cells_coords[:-1]


class ITableExtractor(ABC):
    @abstractmethod
    def extract_tables(
        self,
        image_obj: ImageEntity,
        ocr_engine: str,
        language: str,
    ) -> List[TableEntity]:
        pass


class IBBoxIdentifier(ABC):
    @abstractmethod
    def identify_borders(self, img: np.ndarray) -> List[BoundingBoxEntity]:
        pass


class IOCRService(ABC):
    @abstractmethod
    def extract_data(
        self,
        image_obj: ImageEntity,
        engine: str,
        language: str = DEFAULT_LANGUAGE,
        bbox: Optional[RectangleEntity] = None,
    ) -> List[TextLineEntity]:
        pass

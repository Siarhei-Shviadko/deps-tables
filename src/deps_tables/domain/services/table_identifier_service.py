from typing import List

import numpy as np

from deps_tables.domain.entities import BoundingBoxEntity
from deps_tables.domain.entities.table_detector import TableDetectorInitSettings


class TableIdentifierService:
    def __init__(
        self,
        table_identifier_cls: TableDetectorInitSettings,
        enable_table_identifier: bool = True,
    ):
        self.enabled = False

        if enable_table_identifier:
            self.table_identifier = table_identifier_cls.detector_cls(*table_identifier_cls.detector_args)
            self.enabled = True

    def is_table_on_page(self, page: np.ndarray) -> bool:
        if self.enabled:
            return self.table_identifier.is_table_on_image(page)
        return True

    def identify_table_borders(self, page: np.ndarray) -> List[BoundingBoxEntity]:
        if self.enabled:
            return self.table_identifier.identify_borders(page)
        return []

from operator import attrgetter
from statistics import mean
from typing import List, Tuple

from pydantic import BaseModel

from .ocr_types_v2 import BboxModel, TextLineModel, WordBoxModel


class OCRV3ResultModel(BaseModel):
    textlines: List[TextLineModel]

    class Config:
        allow_population_by_field_name = True

    def extract_text_in_area(self, area: BboxModel, threshold: float = 0.6) -> Tuple[str, float]:
        intersected_words = self._find_intersected_words(area, threshold=threshold)
        return self.compose_text(intersected_words)

    def _find_intersected_words(self, area: BboxModel, threshold: float = 0.6) -> List[WordBoxModel]:
        intersected_words = []
        for textline in self.textlines:
            for word in textline.word_boxes:
                if self.is_intersected_by_box(area, word.bbox, threshold=threshold):
                    intersected_words.append(word)
        return intersected_words

    def compose_text(self, words: List[WordBoxModel]) -> Tuple[str, float]:  # noqa: WPS473
        lines = []

        word_set = words[:]
        mean_confidence = mean(map(attrgetter("confidence"), words)) if words else 0

        while len(word_set) != 0:  # noqa: WPS507
            top_word = min(word_set, key=lambda word: word.bbox.centery)

            intersected_words = [word for word in word_set if self.is_intersected_by_y(top_word.bbox, word.bbox)]
            intersected_words = sorted(intersected_words, key=lambda word: word.bbox.centerx)

            line = " ".join([word.content.strip() for word in intersected_words])

            lines.append(line)

            for word in intersected_words:
                word_set.remove(word)

        text = "\n".join(lines)

        return text, mean_confidence

    @staticmethod
    def is_intersected_by_box(b1: BboxModel, b2: BboxModel, threshold: float = 0.6) -> bool:
        outer_inter = min(b1.h * b1.w, b2.h * b2.w)

        x_inter = max(0.0, min(b1.right, b2.right) - max(b1.left, b2.left))
        y_inter = max(0.0, min(b1.bottom, b2.bottom) - max(b1.top, b2.top))
        inner_inter = x_inter * y_inter

        if outer_inter == 0:
            return False

        intersect_ratio = inner_inter / outer_inter

        return intersect_ratio >= threshold

    @staticmethod
    def is_intersected_by_y(r1: BboxModel, r2: BboxModel, threshold: float = 0.6) -> bool:
        outer_inter = min(r1.h, r2.h)
        inner_inter = max(0.0, min(r1.bottom, r2.bottom) - max(r1.top, r2.top))

        if outer_inter == 0:
            return False

        intersect_ratio = inner_inter / outer_inter

        return intersect_ratio >= threshold

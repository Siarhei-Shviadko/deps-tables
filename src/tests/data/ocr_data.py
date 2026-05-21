from deps_tables.domain.entities import (
    PointEntity,
    RectangleEntity,
    TextLineEntity,
    WordBoxEntity,
)
from deps_tables.events_handler.models import ParsedTextLineModel

ocr_data = [
    {
        "id": 0,
        "wordBoxes": [
            {
                "value": "ads",
                "coordinates": {
                    "x": 0.12784313725490196,
                    "y": 0.11393939393939394,
                    "w": 0.023529411764705882,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.9164655303955078,
                "sourceId": "123",
            },
            {
                "value": "13212",
                "coordinates": {
                    "x": 0.2811764705882353,
                    "y": 0.11424242424242424,
                    "w": 0.04274509803921569,
                    "h": 0.00909090909090909,
                },
                "confidence": 0.9544355773925781,
                "sourceId": "123",
            },
            {
                "value": "ewqsd",
                "coordinates": {
                    "x": 0.7392156862745098,
                    "y": 0.11393939393939394,
                    "w": 0.04549019607843137,
                    "h": 0.011818181818181818,
                },
                "confidence": 0.9054547882080078,
                "sourceId": "123",
            },
        ],
    },
    {
        "id": 1,
        "wordBoxes": [
            {
                "value": "adsda",
                "coordinates": {
                    "x": 0.12784313725490196,
                    "y": 0.1315151515151515,
                    "w": 0.041176470588235294,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.9134928131103516,
                "sourceId": "123",
            },
            {
                "value": "adsda",
                "coordinates": {
                    "x": 0.2807843137254902,
                    "y": 0.1315151515151515,
                    "w": 0.0407843137254902,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.8996561431884765,
                "sourceId": "123",
            },
            {
                "value": "ff",
                "coordinates": {
                    "x": 0.4329411764705882,
                    "y": 0.1315151515151515,
                    "w": 0.010980392156862745,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.6406100463867187,
                "sourceId": "123",
            },
        ],
    },
    {
        "id": 2,
        "wordBoxes": [
            {
                "value": "sda",
                "coordinates": {
                    "x": 0.43333333333333335,
                    "y": 0.14909090909090908,
                    "w": 0.023137254901960783,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.9306084442138672,
                "sourceId": "123",
            },
            {
                "value": "wee",
                "coordinates": {
                    "x": 0.7388235294117647,
                    "y": 0.15181818181818182,
                    "w": 0.02980392156862745,
                    "h": 0.006666666666666667,
                },
                "confidence": 0.9051193237304688,
                "sourceId": "123",
            },
        ],
    },
    {
        "id": 3,
        "wordBoxes": [
            {
                "value": "C",
                "coordinates": {
                    "x": 0.43333333333333335,
                    "y": 0.1693939393939394,
                    "w": 0.006274509803921568,
                    "h": 0.006666666666666667,
                },
                "confidence": 0.3409825134277344,
                "sourceId": "123",
            },
            {
                "value": "XC",
                "coordinates": {
                    "x": 0.5858823529411765,
                    "y": 0.1693939393939394,
                    "w": 0.01411764705882353,
                    "h": 0.006666666666666667,
                },
                "confidence": 0.8511916351318359,
                "sourceId": "123",
            },
        ],
    },
    {
        "id": 4,
        "wordBoxes": [
            {
                "value": "adsa",
                "coordinates": {
                    "x": 0.2807843137254902,
                    "y": 0.18424242424242424,
                    "w": 0.03137254901960784,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.9175747680664063,
                "sourceId": "123",
            },
            {
                "value": "Xaz",
                "coordinates": {
                    "x": 0.43333333333333335,
                    "y": 0.18696969696969698,
                    "w": 0.02235294117647059,
                    "h": 0.006666666666666667,
                },
                "confidence": 0.7203623962402343,
                "sourceId": "123",
            },
            {
                "value": "ddsa",
                "coordinates": {
                    "x": 0.7392156862745098,
                    "y": 0.18424242424242424,
                    "w": 0.032549019607843135,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.915322036743164,
                "sourceId": "123",
            },
        ],
    },
    {
        "id": 5,
        "wordBoxes": [
            {
                "value": "sdsa",
                "coordinates": {
                    "x": 0.2803921568627451,
                    "y": 0.2018181818181818,
                    "w": 0.03019607843137255,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.8539674377441406,
                "sourceId": "123",
            },
            {
                "value": "|o#",
                "coordinates": {
                    "x": 0.5874509803921568,
                    "y": 0.2018181818181818,
                    "w": 0.02862745098039216,
                    "h": 0.01090909090909091,
                },
                "confidence": 0,
                "sourceId": "123",
            },
        ],
    },
    {
        "id": 6,
        "wordBoxes": [
            {
                "value": "fdf",
                "coordinates": {
                    "x": 0.4329411764705882,
                    "y": 0.2193939393939394,
                    "w": 0.0203921568627451,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.9274103546142578,
                "sourceId": "123",
            },
            {
                "value": "132",
                "coordinates": {
                    "x": 0.5866666666666667,
                    "y": 0.2196969696969697,
                    "w": 0.024705882352941175,
                    "h": 0.00909090909090909,
                },
                "confidence": 0.9698178863525391,
                "sourceId": "123",
            },
            {
                "value": "@#@#",
                "coordinates": {
                    "x": 0.7407843137254903,
                    "y": 0.2193939393939394,
                    "w": 0.05333333333333334,
                    "h": 0.01090909090909091,
                },
                "confidence": 0.13509071350097657,
                "sourceId": "123",
            },
        ],
    },
]

wrong_ocr_data = [
    {
        "i": 0,
        "wodBoxes": [
            {
                "value": "ads",
                "coordinates": {
                    "x": 0.12784313725490196,
                    "y": 0.11393939393939394,
                    "w": 0.023529411764705882,
                    "h": 0.009393939393939394,
                },
                "confidence": 0.9164655303955078,
                "sourceId": "123",
            },
            {
                "conent": "13212",
                "coordinates": {
                    "y": 0.11424242424242424,
                    "w": 0.04274509803921569,
                    "h": 0.00909090909090909,
                },
                "confidence": 0.9544355773925781,
                "sourceId": "123",
            },
        ],
    },
]

text_line_models = [ParsedTextLineModel(**data).to_text_line_model() for data in ocr_data]

full_converted_result = [
    TextLineEntity(
        id=0,
        word_boxes=[
            WordBoxEntity(
                content="ads",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=326, y=376),
                    right_bottom_point=PointEntity(x=386, y=407),
                ),
                confidence=0.9164655303955078,
            ),
            WordBoxEntity(
                content="13212",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=717, y=377),
                    right_bottom_point=PointEntity(x=826, y=407),
                ),
                confidence=0.9544355773925781,
            ),
            WordBoxEntity(
                content="ewqsd",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1885, y=376),
                    right_bottom_point=PointEntity(x=2001, y=415),
                ),
                confidence=0.9054547882080078,
            ),
        ],
    ),
    TextLineEntity(
        id=1,
        word_boxes=[
            WordBoxEntity(
                content="adsda",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=326, y=433),
                    right_bottom_point=PointEntity(x=430, y=465),
                ),
                confidence=0.9134928131103516,
            ),
            WordBoxEntity(
                content="adsda",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=716, y=433),
                    right_bottom_point=PointEntity(x=819, y=465),
                ),
                confidence=0.8996561431884765,
            ),
            WordBoxEntity(
                content="ff",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1104, y=433),
                    right_bottom_point=PointEntity(x=1132, y=465),
                ),
                confidence=0.6406100463867187,
            ),
        ],
    ),
    TextLineEntity(
        id=2,
        word_boxes=[
            WordBoxEntity(
                content="sda",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1105, y=491),
                    right_bottom_point=PointEntity(x=1164, y=523),
                ),
                confidence=0.9306084442138672,
            ),
            WordBoxEntity(
                content="wee",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1883, y=501),
                    right_bottom_point=PointEntity(x=1959, y=523),
                ),
                confidence=0.9051193237304688,
            ),
        ],
    ),
    TextLineEntity(
        id=3,
        word_boxes=[
            WordBoxEntity(
                content="C",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1105, y=559),
                    right_bottom_point=PointEntity(x=1121, y=581),
                ),
                confidence=0.3409825134277344,
            ),
            WordBoxEntity(
                content="XC",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1494, y=559),
                    right_bottom_point=PointEntity(x=1530, y=581),
                ),
                confidence=0.8511916351318359,
            ),
        ],
    ),
    TextLineEntity(
        id=4,
        word_boxes=[
            WordBoxEntity(
                content="adsa",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=716, y=608),
                    right_bottom_point=PointEntity(x=796, y=639),
                ),
                confidence=0.9175747680664063,
            ),
            WordBoxEntity(
                content="Xaz",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1105, y=617),
                    right_bottom_point=PointEntity(x=1162, y=639),
                ),
                confidence=0.7203623962402343,
            ),
            WordBoxEntity(
                content="ddsa",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1885, y=608),
                    right_bottom_point=PointEntity(x=1968, y=639),
                ),
                confidence=0.915322036743164,
            ),
        ],
    ),
    TextLineEntity(
        id=5,
        word_boxes=[
            WordBoxEntity(
                content="sdsa",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=715, y=666),
                    right_bottom_point=PointEntity(x=792, y=697),
                ),
                confidence=0.8539674377441406,
            ),
            WordBoxEntity(
                content="|o#",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1498, y=666),
                    right_bottom_point=PointEntity(x=1571, y=701),
                ),
                confidence=0.0,
            ),
        ],
    ),
    TextLineEntity(
        id=6,
        word_boxes=[
            WordBoxEntity(
                content="fdf",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1104, y=724),
                    right_bottom_point=PointEntity(x=1156, y=755),
                ),
                confidence=0.9274103546142578,
            ),
            WordBoxEntity(
                content="132",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1496, y=725),
                    right_bottom_point=PointEntity(x=1559, y=755),
                ),
                confidence=0.9698178863525391,
            ),
            WordBoxEntity(
                content="@#@#",
                bbox=RectangleEntity(
                    left_top_point=PointEntity(x=1889, y=724),
                    right_bottom_point=PointEntity(x=2025, y=760),
                ),
                confidence=0.13509071350097657,
            ),
        ],
    ),
]

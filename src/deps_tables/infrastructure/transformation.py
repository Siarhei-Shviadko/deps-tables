import cv2
import numpy as np


def rotate_image(image: np.ndarray, rotation_angle: int) -> np.ndarray:
    rotation_mapping = {  # noqa: WPS417
        -90: cv2.ROTATE_90_COUNTERCLOCKWISE,
        180: cv2.ROTATE_180,
        90: cv2.ROTATE_90_CLOCKWISE,
    }
    if rotation_angle in rotation_mapping:
        image = cv2.rotate(image, rotation_mapping.get(rotation_angle))
    return image

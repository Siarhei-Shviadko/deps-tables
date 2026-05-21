from typing import Optional

import cv2
import numpy as np
from dependency_injector.wiring import Provide, inject
from fastapi import Body, Depends, HTTPException, status

from deps_tables.api.models.image import ImageMetadataModel, ImageModel
from deps_tables.api.models.transfromations import TransformationSchema
from deps_tables.containers import Application
from deps_tables.domain.exceptions import ImageLoadError
from deps_tables.extras.services import StorageControllerService
from deps_tables.infrastructure.transformation import rotate_image


@inject
def get_file_from_storage(
    file_info: str = Body(..., alias="blobFile"),
    transformations: Optional[TransformationSchema] = Body(None),
    storage: StorageControllerService = Depends(Provide[Application.external_services.storage_controller_service]),
) -> ImageModel:
    try:
        file_content = storage.download_content(file_path=file_info)
        image_meta = ImageMetadataModel(**storage.load_metadata(file_path=file_info))
        np_array = np.frombuffer(file_content, dtype=np.uint8)
        cv2_image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)

        image = ImageModel(image=cv2_image, blob_path=file_info, meta=image_meta)
        cv2_image = image.image
        if transformations:
            cv2_image = rotate_image(cv2_image, transformations.rotation.value)

        image.image = cv2_image
    except ImageLoadError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Image wasn't loaded")

    return image

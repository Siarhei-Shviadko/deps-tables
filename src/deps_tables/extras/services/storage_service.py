import json
import os
import tempfile
import uuid
from io import BytesIO
from typing import Any, Dict, Optional

from ..drivers.auth_driver import AuthDriverMixin
from .exceptions import FileStorageRequestError


class StorageControllerService(AuthDriverMixin):  # noqa: WPS214
    """
    Sends requests to File Storage API.

    Raises:
        FileStorageRequestError: if response status code is not 200.
    """

    def __init__(
        self,
        file_storage_url: str,
        verify_ssl: bool = False,
        storage: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        """
        Args:
            file_storage_url (str): File Storage API url.
            verify_ssl (bool, optional): Enable SSL certificates checking during requests (default is False).
            auth_enabled (bool, optional): Enable authorization (default is False).
            storage (str, optional): Storage name (default is None). Will be used by default in all requests.
            If None is set will use file storage service default
            api_key (str, optional): API key for public services authorization (default is None).
        """
        super(StorageControllerService, self).__init__(access_token=access_token)  # noqa: WPS608
        self._file_storage_url = file_storage_url
        self._storage = storage
        self._verify_ssl = verify_ssl

    def upload_file(self, file_path: str, source_path: str, storage: Optional[str] = None) -> str:
        """
        Uploads new file to File Storage.

        Args:
            file_path (str): Path to the file in File Storage where file content will be uploaded to.
            source_path (str): Path to the file you need to upload.
            storage (str, optional): Storage name (default is None).

        Returns:
            str: Path to the file in File Storage.
        """
        file_path, filename = os.path.split(file_path)
        with open(source_path, "rb") as fp:
            return self._upload_file(
                file_path,
                filename,
                fp,
                storage or self._storage,
                replace_if_exists=True,
            )

    def upload_content(
        self,
        file_path: str,
        content: bytes,
        storage: Optional[str] = None,
        generate_unique_filename: bool = True,
    ) -> str:
        """
        Uploads new content to File Storage.

        Args:
            file_path (str): Path to the file in File Storage where content will be uploaded to.
            content (bytes): Content that you need to upload.
            storage (str, optional): Storage name (default is None).
            generate_unique_filename (bool, optional): Generate unique filename for uploading file (default is True).
            If True, filename from file_path parameter will be modified.

        Returns:
            str: Path to the file in File Storage with uploaded content.
        """
        if generate_unique_filename:
            file_path = self._generate_unique_file_path(file_path)
        file_path, filename = os.path.split(file_path)

        return self._upload_file(
            file_path,
            filename,
            BytesIO(content),
            storage or self._storage,
            replace_if_exists=True,
        )

    def download_file(self, file_path: str, destination_path: str, storage: Optional[str] = None) -> None:
        """
        Downloads file from File Storage.

        Args:
            file_path (str): Path to the file in File Storage which content you need to download.
            destination_path (str): Path to the file where downloaded content will be saved.
            storage (str, optional): Storage name (default is None).

        Returns:
            None
        """
        content = self.download_content(file_path, storage or self._storage)

        with open(destination_path, "wb") as fp:
            fp.write(content)

    def download_content(self, file_path: str, storage: Optional[str] = None) -> bytes:
        """
        Downloads content from File Storage.

        Args:
            file_path (str): Path to the file in File Storage which content you need to download.
            storage (str, optional): Storage name (default is None).

        Returns:
            bytes: Downloaded content.
        """
        response = self._session.get(
            self._get_url(file_path),
            params={"storage": storage or self._storage},
            verify=self._verify_ssl,
        )
        self._handle_response_errors(response)
        return response.content

    def delete_file(self, file_path: str, storage: Optional[str] = None) -> None:
        """
        Deletes file from File Storage.

        Args:
            file_path (str): Path to the file in File Storage you need to delete.
            storage (str, optional): Storage name (default is None).

        Returns:
            None
        """
        response = self._session.delete(
            self._get_url(file_path),
            data={"storage": storage or self._storage},
            verify=self._verify_ssl,
        )
        self._handle_response_errors(response)

    def _upload_file(
        self,
        file_path: str,
        filename: str,
        file_object,
        storage: Optional[str],
        replace_if_exists=False,
    ):
        """Sends POST-request to upload new file."""
        file = {
            "file": (filename, file_object),
        }
        response = self._session.post(
            self._get_url(file_path),
            files=file,
            data={"replaceIfExists": replace_if_exists, "storage": storage},
            verify=self._verify_ssl,
        )
        self._handle_response_errors(response)

        response_json = response.json()
        return response_json["path"]

    def _get_url(self, file_path):
        """Generates full path to the file folder in File Storage."""
        return "/".join((self._file_storage_url, file_path)).rstrip("/")

    @staticmethod
    def _handle_response_errors(response):
        """Handles http-errors."""
        if not response.ok:
            raise FileStorageRequestError(f"File storage service returned {response.status_code} code: {response.text}")

    @staticmethod
    def _generate_unique_file_path(file_path: str) -> str:
        """Generates unique file path."""
        root, file_name = os.path.split(file_path)
        _, ext = os.path.splitext(file_name)

        return os.path.join(root, str(uuid.uuid4().hex) + ext)

    def load_metadata(self, file_path: str, storage: Optional[str] = None) -> Dict[str, Any]:
        """
        Downloads file metadata.

        Args:
             file_path (str): Path to the file in File Storage which metadata you need to download.
             storage (str, optional): Storage name (default is None).

        Returns:
            ImageFileMetadataObject: Metadata object.
        """
        metadata_path = self._get_metadata_path(file_path)

        try:
            content = self.download_content(metadata_path, storage or self._storage)
            json_str = content.decode("utf8")
            metadata = json.loads(json_str)
        except FileStorageRequestError:
            metadata = {}

        return metadata

    def upload_metadata(
        self,
        file_path: str,
        metadata: Dict[str, Any],
        storage: Optional[str] = None,
    ) -> None:
        """
        Uploads file metadata to File Storage.

        Args:
            file_path (str): Path to the file in File Storage which metadata you need to upload.
            metadata (ImageFileMetadataObject): Metadata object to upload.
            storage (str, optional): Storage name (default is None).

        Returns:
            None
        """
        metadata_path = self._get_metadata_path(file_path)

        file_metadata = self.load_metadata(file_path, storage=storage)
        file_metadata.update(metadata)

        json_str = json.dumps(file_metadata)
        content = json_str.encode("utf8")

        with tempfile.NamedTemporaryFile() as fp:
            fp.write(content)
            fp.flush()
            self.upload_file(metadata_path, fp.name, storage or self._storage)

    def delete_metadata(self, file_path: str, storage: Optional[str] = None) -> None:
        """
        Deletes file metadata from File Storage.

        Args:
            file_path: Path to the file in File Storage which metadata you need to delete.
            storage (str, optional): Storage name (default is None).

        Returns:
            None
        """
        metadata_path = self._get_metadata_path(file_path)

        self.delete_file(metadata_path, storage or self._storage)

    @staticmethod
    def _get_metadata_path(file_path: str) -> str:
        """Gets path to metadata from filepath"""
        dir_path, filename = os.path.split(file_path)
        filename, _ = os.path.splitext(filename)

        metadata_filename = "metadata_{}.json".format(filename)  # noqa: P101
        return os.path.join(dir_path, metadata_filename)

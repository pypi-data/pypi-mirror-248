from io import BytesIO
from typing import IO, Optional
from uuid import uuid4

from google.cloud import storage

from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage


class GoogleCloudStorage(IFileStorage):
    def __init__(
        self, project_id: str, bucket_name: str, file_prefix: str = "", client: Optional[storage.Client] = None
    ) -> None:
        self.client = client or storage.Client(project=project_id)
        self.bucket_name = bucket_name
        self.file_prefix = file_prefix

    def save_file(self, file: IO) -> str:
        file_id = str(uuid4())
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.file_prefix + file_id)
        blob.upload_from_file(file)
        return file_id

    def get_file(self, file_id: str) -> IO:
        bucket = self.client.get_bucket(self.bucket_name)
        blob = bucket.blob(self.file_prefix + file_id)
        return BytesIO(blob.download_as_bytes())

    @classmethod
    def build_from_config(cls) -> "GoogleCloudStorage":
        from speech_recognition_api.extra.google_cloud_storage.config import (  # noqa: PLC0415
            google_cloud_storage_config,
        )

        return cls(
            project_id=google_cloud_storage_config.project_id,
            bucket_name=google_cloud_storage_config.bucket_name,
            file_prefix=google_cloud_storage_config.file_prefix,
        )

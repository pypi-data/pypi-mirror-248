from io import BytesIO
from typing import IO, Optional
from uuid import uuid4

import boto3
from boto3_type_annotations.s3 import ServiceResource

from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage


class S3Storage(IFileStorage):
    def __init__(
        self,
        bucket_name: str,
        file_prefix: str = "",
        resource: Optional[ServiceResource] = None,
    ) -> None:
        if not resource:
            resource = boto3.resource("s3")
        self.resource: ServiceResource = resource
        self.bucket = resource.Bucket(bucket_name)
        self.file_prefix = file_prefix

    def save_file(self, file: IO) -> str:
        file_id = str(uuid4())
        self.bucket.upload_fileobj(Fileobj=file, Key=self.file_prefix + file_id)
        return file_id

    def get_file(self, file_id: str) -> IO:
        file = BytesIO()
        self.bucket.download_fileobj(Fileobj=file, Key=self.file_prefix + file_id)
        file.seek(0)
        return file

    @classmethod
    def build_from_config(cls) -> "S3Storage":
        from speech_recognition_api.extra.s3_storage.config import s3_storage_config  # noqa: PLC0415

        return cls(
            bucket_name=s3_storage_config.bucket_name,
            file_prefix=s3_storage_config.file_prefix,
        )

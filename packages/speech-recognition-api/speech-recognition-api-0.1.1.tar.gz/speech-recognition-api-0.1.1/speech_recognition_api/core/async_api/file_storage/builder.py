from typing import ClassVar

from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage
from speech_recognition_api.core.common.utils import build_from_class_path
from speech_recognition_api.core.config import app_config


class FileStorageBuilder:
    storage: ClassVar[IFileStorage]

    @classmethod
    def build(cls) -> IFileStorage:
        if not hasattr(cls, "storage"):
            cls.storage = build_from_class_path(app_config.storage)
        return cls.storage

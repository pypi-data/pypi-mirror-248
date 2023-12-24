from abc import abstractmethod
from typing import IO

from speech_recognition_api.core.common.buildable import Buildable


class IFileStorage(Buildable["IFileStorage"]):
    @abstractmethod
    def save_file(self, file: IO) -> str:
        ...

    @abstractmethod
    def get_file(self, file_id: str) -> IO:
        ...

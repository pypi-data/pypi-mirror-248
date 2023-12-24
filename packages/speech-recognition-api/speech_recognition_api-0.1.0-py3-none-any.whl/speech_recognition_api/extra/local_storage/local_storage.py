from io import BytesIO
from pathlib import Path
from typing import IO, Union
from uuid import uuid4

from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage


class LocalStorage(IFileStorage):
    def __init__(self, folder_path: Union[Path, str]) -> None:
        if isinstance(folder_path, str):
            folder_path = Path(folder_path)
        self.folder_path = folder_path  # TODO: add checks

    def save_file(self, file: IO) -> str:
        name = str(uuid4())
        with (self.folder_path / name).open("wb") as output_file:
            for b in file:
                output_file.write(b)
        return name

    def get_file(self, file_id: str) -> IO:
        with (self.folder_path / file_id).open("rb") as file:
            output = file.read()
        return BytesIO(output)

    @classmethod
    def build_from_config(cls) -> "LocalStorage":
        from speech_recognition_api.extra.local_storage.config import local_storage_config  # noqa: PLC0415

        return cls(folder_path=local_storage_config.folder_path)

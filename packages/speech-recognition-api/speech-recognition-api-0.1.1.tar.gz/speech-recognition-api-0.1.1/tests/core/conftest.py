from io import BytesIO
from typing import IO, Optional
from uuid import uuid4

import pytest
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env.test"), override=True)

from speech_recognition_api.core.async_api.async_api import async_router
from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage
from speech_recognition_api.core.async_api.message_bus.interface import IMessageBus
from speech_recognition_api.core.async_api.worker import process_file
from speech_recognition_api.core.common.model.interface import ISpeechRecognitionModel
from speech_recognition_api.core.sync_api.sync_api import sync_router


class DummyModel(ISpeechRecognitionModel):
    def __init__(self, return_string: Optional[str] = "Test"):
        self.return_string = return_string

    def process_file(self, file: IO) -> str:
        return self.return_string

    @classmethod
    def build_from_config(cls) -> "DummyModel":
        return cls()


class DummyFileStorage(IFileStorage):
    def save_file(self, file: IO) -> str:
        return str(uuid4())

    def get_file(self, file_id: str) -> IO:
        return BytesIO()

    @classmethod
    def build_from_config(cls) -> "DummyFileStorage":
        return cls()


class DummyMessageBus(IMessageBus):
    def __init__(self):
        self.tasks = {"test_task_id": {"status": "SUCCESS", "result": "Test"}}

    def create_task(self, file_id: str) -> str:
        return "test_task_id"

    def get_task_status(self, task_id: str) -> str:
        return self.tasks[task_id]["status"]

    def get_task_result(self, task_id: str) -> str:
        return self.tasks[task_id]["result"]

    @classmethod
    def build_from_config(cls) -> "DummyMessageBus":
        return cls()


@pytest.fixture()
def dummy_sync_router():
    return sync_router


@pytest.fixture()
def dummy_async_router():
    return async_router


@pytest.fixture()
def dummy_async_worker():
    return process_file

from abc import abstractmethod
from typing import Literal

from speech_recognition_api.core.common.buildable import Buildable

SUCCESS = "SUCCESS"
PENDING = "PENDING"
FAILED = "FAILED"

TASK_STATUS = Literal["SUCCESS", "PENDING", "FAILED"]


class IMessageBus(Buildable["IMessageBus"]):
    @abstractmethod
    def create_task(self, file_id: str) -> str:
        ...

    @abstractmethod
    def get_task_status(self, task_id: str) -> TASK_STATUS:
        ...

    @abstractmethod
    def get_task_result(self, task_id: str) -> str:
        ...

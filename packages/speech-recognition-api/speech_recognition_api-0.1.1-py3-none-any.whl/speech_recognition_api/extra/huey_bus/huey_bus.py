import warnings
from typing import Optional

from huey import RedisHuey
from huey.api import Huey, MemoryHuey, Result, TaskWrapper
from huey.exceptions import ConfigurationError

from speech_recognition_api.core.async_api.message_bus.interface import TASK_STATUS, IMessageBus
from speech_recognition_api.core.async_api.worker import process_file
from speech_recognition_api.extra.huey_bus.config import huey_bus_config

try:
    huey = RedisHuey(name=huey_bus_config.name, host=huey_bus_config.redis_host)
except ConfigurationError:
    warnings.warn("Falling back to in-memory huey, please install redis package to use RedisHuey.", stacklevel=1)
    huey = MemoryHuey()


@huey.task()
def huey_task(file_id: str) -> Result:
    return process_file(file_id)


class HueyMessageBus(IMessageBus):
    def __init__(self, app: Optional[Huey] = None, task: Optional[TaskWrapper] = None) -> None:
        self.app = app if app is not None else huey
        self.task = task or huey_task

    def create_task(self, file_id: str) -> str:
        result = self.task(file_id)
        return result.id

    def get_task_status(self, task_id: str) -> TASK_STATUS:
        result = self.app.result(task_id, preserve=True)
        if not result:
            return "PENDING"
        return "SUCCESS"

    def get_task_result(self, task_id: str) -> str:
        return self.app.result(task_id, preserve=True).get("transcription")

    @classmethod
    def build_from_config(cls) -> "HueyMessageBus":
        return HueyMessageBus()

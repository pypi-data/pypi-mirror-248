from typing import Optional

from celery import Celery
from celery.local import PromiseProxy
from celery.result import AsyncResult

from speech_recognition_api.core.async_api.message_bus.interface import TASK_STATUS, IMessageBus
from speech_recognition_api.core.async_api.worker import process_file
from speech_recognition_api.extra.celery_bus.config import celery_bus_config

celery = Celery(
    main=celery_bus_config.name,
    broker=celery_bus_config.broker,
    backend=celery_bus_config.backend,
)


@celery.task()
def celery_task(file_id: str) -> dict[str, str]:
    return process_file(file_id)


class CeleryMessageBus(IMessageBus):
    def __init__(self, app: Optional[Celery] = None, task: Optional[PromiseProxy] = None) -> None:
        self.celery_app = app or celery
        self.task = task or celery_task

    def create_task(self, file_id: str) -> str:
        result = self.task.delay(file_id)
        return result.id

    def get_task_status(self, task_id: str) -> TASK_STATUS:
        result = AsyncResult(task_id, app=self.celery_app)
        return result.status

    def get_task_result(self, task_id: str) -> str:
        result = AsyncResult(task_id, app=self.celery_app)
        return result.get().get("transcription")

    @classmethod
    def build_from_config(cls) -> "CeleryMessageBus":
        return CeleryMessageBus()

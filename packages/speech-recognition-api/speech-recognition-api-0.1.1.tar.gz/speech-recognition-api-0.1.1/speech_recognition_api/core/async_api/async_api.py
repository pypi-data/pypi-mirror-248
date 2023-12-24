from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, File

from speech_recognition_api.core.async_api.dependencies import get_message_bus, get_storage
from speech_recognition_api.core.async_api.dto import CreateTranscriptionTaskResponse, GetTranscriptionTaskResponse
from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage
from speech_recognition_api.core.async_api.message_bus.interface import IMessageBus

async_router = APIRouter(prefix="/async/v1", tags=["Async"])

SUCCESS = "SUCCESS"
PENDING = "PENDING"


@async_router.post("/transcribe")
def create_task(
    file: Annotated[bytes, File()],
    storage: IFileStorage = Depends(get_storage),
    message_bus: IMessageBus = Depends(get_message_bus),
) -> CreateTranscriptionTaskResponse:
    file_id = storage.save_file(BytesIO(file))
    task_id = message_bus.create_task(file_id)
    return CreateTranscriptionTaskResponse(task_id=task_id)


@async_router.get("/transcribe/{task_id}")
def get_task_result(task_id: str, message_bus: IMessageBus = Depends(get_message_bus)) -> GetTranscriptionTaskResponse:
    status = message_bus.get_task_status(task_id)
    transcription = None
    if status == SUCCESS:
        transcription = message_bus.get_task_result(task_id)
    return GetTranscriptionTaskResponse(status=status, transcription=transcription)

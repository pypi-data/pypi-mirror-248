from fastapi import APIRouter, Depends, UploadFile

from speech_recognition_api.core.common.model.interface import ISpeechRecognitionModel
from speech_recognition_api.core.sync_api.dependencies import get_model
from speech_recognition_api.core.sync_api.dto import TranscriptionResponse

sync_router = APIRouter(prefix="/sync/v1", tags=["Sync"])


@sync_router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile, model: ISpeechRecognitionModel = Depends(get_model)
) -> TranscriptionResponse:
    transcription = model.process_file(file.file)
    return TranscriptionResponse(transcription=transcription)

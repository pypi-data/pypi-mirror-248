from typing import Optional

from pydantic import BaseModel


class CreateTranscriptionTaskResponse(BaseModel):
    task_id: str


class GetTranscriptionTaskResponse(BaseModel):
    status: str
    transcription: Optional[str] = None

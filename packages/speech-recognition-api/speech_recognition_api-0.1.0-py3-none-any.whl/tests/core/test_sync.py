from io import BytesIO

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_sync_router_transcribe(dummy_sync_router):
    app = FastAPI()
    app.include_router(dummy_sync_router)

    with TestClient(app) as client:
        response = client.post("sync/v1/transcribe", files={"file": ("test.mp3", BytesIO())})
        assert response.status_code == 200

        response_body = response.json()
        assert response_body["transcription"] == "Test"

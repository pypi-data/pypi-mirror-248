from io import BytesIO

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_sync_router_transcribe_create_task(dummy_async_router):
    app = FastAPI()
    app.include_router(dummy_async_router)

    with TestClient(app) as client:
        response = client.post("async/v1/transcribe", files={"file": ("test.mp3", BytesIO())})
        assert response.status_code == 200

        response_body = response.json()
        task_id = response_body.get("task_id")
        assert task_id == "test_task_id"


def test_sync_router_transcribe_get_task(dummy_async_router):
    app = FastAPI()
    app.include_router(dummy_async_router)

    task_id = "test_task_id"
    with TestClient(app) as client:
        response = client.get(f"async/v1/transcribe/{task_id}")
        assert response.status_code == 200

        response_body = response.json()
        assert response_body["transcription"] == "Test"


def test_worker(dummy_async_worker):
    result = dummy_async_worker(file_id="test_file_id")
    assert result["transcription"] == "Test"

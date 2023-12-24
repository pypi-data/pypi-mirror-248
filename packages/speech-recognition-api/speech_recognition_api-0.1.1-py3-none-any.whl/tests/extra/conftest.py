from pathlib import Path
from unittest.mock import MagicMock

import pytest
from huey import MemoryHuey

from speech_recognition_api.extra.celery_bus import CeleryMessageBus
from speech_recognition_api.extra.google_cloud_storage import GoogleCloudStorage
from speech_recognition_api.extra.huey_bus import HueyMessageBus
from speech_recognition_api.extra.local_storage import LocalStorage
from speech_recognition_api.extra.s3_storage.s3_storage import S3Storage
from speech_recognition_api.extra.whisper_model import WhisperModel

TEST_OUTPUT = "Test"


@pytest.fixture()
def audio_file_generator():
    def file_opener():
        current_dir = Path(__name__).parent
        if current_dir.absolute().match("tests"):
            audio_path = current_dir / "extra" / "test_data" / "audio.wav"
        else:
            audio_path = current_dir / "tests" / "extra" / "test_data" / "audio.wav"
        f = open(audio_path, "rb")
        yield f
        f.close()

    return file_opener


@pytest.fixture()
def whisper_model():
    return WhisperModel(model_name="openai/whisper-tiny.en")


@pytest.fixture()
def local_storage(tmp_path):
    return LocalStorage(tmp_path)


@pytest.fixture()
def google_cloud_storage(audio_file_generator):
    mock_client = MagicMock()
    mock_bucket = MagicMock()
    mock_bucket.blob.return_value.download_as_bytes.return_value = next(audio_file_generator()).read()
    mock_client.get_bucket.return_value = mock_bucket
    return GoogleCloudStorage(project_id="test", bucket_name="test", client=mock_client)


@pytest.fixture()
def s3_storage(audio_file_generator):
    mock_resource = MagicMock()
    mock_bucket = MagicMock()

    def load_into_file(Fileobj, *args, **kwargs):  # noqa: N803
        Fileobj.write(next(audio_file_generator()).read())

    mock_bucket.download_fileobj = load_into_file
    mock_resource.Bucket.return_value = mock_bucket
    return S3Storage(bucket_name="test", resource=mock_resource)


@pytest.fixture()
def celery_config():
    return {"broker_url": "memory://", "result_backend": "db+sqlite:///celery.sqlite"}


@pytest.fixture()
def celery_message_bus(celery_app):
    @celery_app.task()
    def dummy_task(*args, **kwargs):
        return {"transcription": TEST_OUTPUT}

    return CeleryMessageBus(app=celery_app, task=dummy_task)


@pytest.fixture()
def huey_message_bus():
    huey = MemoryHuey(immediate=True)

    @huey.task()
    def dummy_task(*args, **kwargs):
        return {"transcription": TEST_OUTPUT}

    return HueyMessageBus(app=huey, task=dummy_task)

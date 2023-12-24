import pytest

from speech_recognition_api.core.async_api.message_bus.interface import PENDING, SUCCESS
from tests.extra.conftest import TEST_OUTPUT


@pytest.mark.parametrize(
    "message_bus,worker",
    [
        (pytest.lazy_fixture("celery_message_bus"), pytest.lazy_fixture("celery_worker")),
        (pytest.lazy_fixture("huey_message_bus"), None),
    ],
)
def test_message_bus(message_bus, worker):
    task_id = message_bus.create_task("test_file")
    assert task_id is not None
    status = PENDING
    while status == PENDING:
        status = message_bus.get_task_status(task_id)
    assert status == SUCCESS
    transcription = message_bus.get_task_result(task_id)
    assert transcription == TEST_OUTPUT

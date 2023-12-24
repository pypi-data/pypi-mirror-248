import pytest


@pytest.mark.parametrize("model", [pytest.lazy_fixture("whisper_model")])
def test_transcription(model, audio_file_generator):
    transcription = model.process_file(next(audio_file_generator()))
    assert transcription

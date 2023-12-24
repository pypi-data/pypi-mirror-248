from speech_recognition_api.core.async_api.file_storage.builder import FileStorageBuilder
from speech_recognition_api.core.common.model.builder import ModelBuilder


def process_file(file_id: str) -> dict[str, str]:
    storage = FileStorageBuilder.build()
    file = storage.get_file(file_id)
    model = ModelBuilder.build()
    transcription = model.process_file(file)
    return {"transcription": transcription}

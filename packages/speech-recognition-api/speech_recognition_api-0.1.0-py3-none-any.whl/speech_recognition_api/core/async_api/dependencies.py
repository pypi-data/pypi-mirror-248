from speech_recognition_api.core.async_api.file_storage.builder import FileStorageBuilder
from speech_recognition_api.core.async_api.file_storage.interface import IFileStorage
from speech_recognition_api.core.async_api.message_bus.builder import MessageBusBuilder
from speech_recognition_api.core.async_api.message_bus.interface import IMessageBus
from speech_recognition_api.core.common.model.builder import ModelBuilder
from speech_recognition_api.core.common.model.interface import ISpeechRecognitionModel


def get_model() -> ISpeechRecognitionModel:
    return ModelBuilder.build()


def get_storage() -> IFileStorage:
    return FileStorageBuilder.build()


def get_message_bus() -> IMessageBus:
    return MessageBusBuilder.build()

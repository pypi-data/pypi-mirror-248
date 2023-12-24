from speech_recognition_api.core.common.model.builder import ModelBuilder
from speech_recognition_api.core.common.model.interface import ISpeechRecognitionModel


def get_model() -> ISpeechRecognitionModel:
    return ModelBuilder.build()

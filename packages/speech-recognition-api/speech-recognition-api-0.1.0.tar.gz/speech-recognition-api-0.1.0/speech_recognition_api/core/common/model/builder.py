from typing import ClassVar

from speech_recognition_api.core.common.model.interface import ISpeechRecognitionModel
from speech_recognition_api.core.common.utils import build_from_class_path
from speech_recognition_api.core.config import app_config


class ModelBuilder:
    model: ClassVar[ISpeechRecognitionModel]

    @classmethod
    def build(cls) -> ISpeechRecognitionModel:
        if not hasattr(cls, "model"):
            cls.model = build_from_class_path(app_config.model)
        return cls.model

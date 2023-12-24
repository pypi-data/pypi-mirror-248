from abc import abstractmethod
from typing import IO

from speech_recognition_api.core.common.buildable import Buildable


class ISpeechRecognitionModel(Buildable["ISpeechRecognitionModel"]):
    @abstractmethod
    def process_file(self, file: IO) -> str:
        ...

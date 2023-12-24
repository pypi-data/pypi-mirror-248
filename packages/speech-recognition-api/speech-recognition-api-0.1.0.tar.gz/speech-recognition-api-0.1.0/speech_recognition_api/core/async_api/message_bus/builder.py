from typing import ClassVar

from speech_recognition_api.core.async_api.message_bus.interface import IMessageBus
from speech_recognition_api.core.common.utils import build_from_class_path
from speech_recognition_api.core.config import app_config


class MessageBusBuilder:
    message_bus: ClassVar[IMessageBus]

    @classmethod
    def build(cls) -> IMessageBus:
        if not hasattr(cls, "message_bus"):
            cls.message_bus = build_from_class_path(app_config.message_bus)
        return cls.message_bus

from importlib import import_module
from typing import Any

from speech_recognition_api.core.common.buildable import Buildable


def build_from_class_path(class_path: str) -> Any:  # noqa: ANN401
    split_path = class_path.split(".")
    module_path = ".".join(split_path[:-1])
    class_name = split_path[-1]
    module = import_module(module_path)
    klass: Buildable = getattr(module, class_name)
    if not type(klass) != Buildable:
        raise ValueError(f"Class is not buildable: {klass}")
    return klass.build_from_config()

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class Buildable(Generic[T], ABC):
    @classmethod
    @abstractmethod
    def build_from_config(cls) -> T:
        ...

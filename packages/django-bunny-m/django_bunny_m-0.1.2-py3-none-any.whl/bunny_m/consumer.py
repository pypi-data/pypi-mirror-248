from abc import ABC, abstractmethod
from typing import Type, Set, Optional

from bunny_m import BaseEvent
from bunny_m.message import BaseMessageFormat, Message


class BaseConsumer(ABC):
    @classmethod
    @abstractmethod
    def get_event_class(cls) -> Type[BaseEvent]:
        pass

    @abstractmethod
    def handle(self, message) -> None:
        pass


class BaseMessageConsumer(BaseConsumer, ABC):
    @abstractmethod
    def handle(self, message: Message) -> None:
        pass


class BaseDictConsumer(BaseConsumer, ABC):
    @abstractmethod
    def handle(self, message: dict) -> None:
        pass

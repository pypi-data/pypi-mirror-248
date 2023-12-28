from abc import ABC, abstractmethod
from typing import Type

from bunny_m.message import BaseMessageFormat


class BaseEvent(ABC):
    EXCHANGE_TYPE = 'fanout'

    @classmethod
    @abstractmethod
    def get_event_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_message_format(cls) -> BaseMessageFormat:
        pass

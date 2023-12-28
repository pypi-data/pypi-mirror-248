from abc import ABC, abstractmethod
from typing import Type

from bunny_m import BaseEvent, BaseConsumer

from {{ event_class_location }} import {{ event_class_name }}
from {{ message_class_location }} import {{ message_class_name }}


class {{ base_consumer_class_name }}(BaseConsumer, ABC):
    @classmethod
    def get_event_class(cls) -> Type[BaseEvent]:
        return {{ event_class_name }}

    @abstractmethod
    def handle(self, message: {{ message_class_name }}) -> None:
        pass

import importlib
from typing import Optional, List

from bunny_m.consumer import BaseConsumer
from bunny_m.exceptions import ConsumerClassException
from bunny_m.settings import BunnySettings


class ConsumersProvider:
    @classmethod
    def get_consumer_instance(cls, classpath: str) -> BaseConsumer:
        try:
            module_name, class_name = classpath.rsplit(".", 1)
            return getattr(importlib.import_module(module_name), class_name)()
        except Exception as e:
            raise ConsumerClassException(f"{classpath} was not found!") from e

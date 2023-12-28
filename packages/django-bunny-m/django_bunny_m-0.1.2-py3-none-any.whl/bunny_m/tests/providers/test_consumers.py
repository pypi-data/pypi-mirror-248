from typing import Type

from django.test import TestCase

from bunny_m import BaseEvent
from bunny_m.consumer import BaseConsumer
from bunny_m.exceptions import ConsumerClassException
from bunny_m.message import BaseMessageFormat
from bunny_m.providers.consumers import ConsumersProvider


class ExampleConsumer(BaseConsumer):
    @classmethod
    def get_event_class(cls) -> Type[BaseEvent]:
        pass

    def handle(self, message: BaseMessageFormat) -> None:
        pass


class ConsumerProviderTests(TestCase):
    def setUp(self) -> None:
        self.consumers_provider = ConsumersProvider()

    def test_get_consumer_instance(self) -> None:
        class_path = ExampleConsumer().__module__ + '.' + ExampleConsumer().__class__.__name__
        result = self.consumers_provider.get_consumer_instance(class_path)
        self.assertIsInstance(result, ExampleConsumer)

    def test_get_consumer_instance__fail(self) -> None:
        class_path = 'INVALID_CLASS._NAME'
        with self.assertRaises(ConsumerClassException):
            self.consumers_provider.get_consumer_instance(class_path)

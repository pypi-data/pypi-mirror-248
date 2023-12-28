import logging
from unittest.mock import MagicMock, patch

import pika
from django.test import TestCase
from pika import DeliveryMode

from bunny_m import BaseEvent
from bunny_m.services import ProducerManager
from bunny_m.services.base_manager import BaseManager
from bunny_m.settings import BunnySettings
from bunny_m.providers import ConnectionProvider


class ProducerManagerTests(TestCase):
    EVENT_NAME = 'test_event_name'
    DATA = {'data': 'test'}

    def setUp(self) -> None:
        channel = MagicMock()
        channel.confirm_delivery = MagicMock()
        channel.basic_publish = MagicMock()
        connection_provider_mock = MagicMock(spec=ConnectionProvider)
        connection_mock = MagicMock(spec=pika.BlockingConnection)
        connection_mock.channel = MagicMock(return_value=channel)
        connection_provider_mock.get_connection = MagicMock(return_value=connection_mock)
        delivery_callback = MagicMock()
        event_mock = MagicMock(spec=BaseEvent)
        event_mock.get_event_name = MagicMock(return_value=self.EVENT_NAME)
        dump_mock = MagicMock()
        dump_mock.dump = MagicMock(return_value=self.DATA)
        event_mock.get_message_format = MagicMock(return_value=dump_mock)
        self.delivery_callback = delivery_callback
        self.producer = ProducerManager(bunny_settings=self._get_settings_mock(), connection_provider=connection_provider_mock,
                                        delivery_callback=delivery_callback, event_class=event_mock)

        self.producer._channel = channel
        self.channel = channel

    def test_init(self) -> None:
        self.producer.init()
        self.producer._channel = self.channel
        self.channel.confirm_delivery.assert_called_with(callback=self.delivery_callback)

    def test_produce(self) -> None:
        self.producer.produce({'data': 'test'})
        properties = pika.BasicProperties(content_type=ProducerManager.CONTENT_TYPE,
                                          delivery_mode=DeliveryMode.Persistent)
        self.channel.basic_publish.assert_called_with(self.EVENT_NAME, '', b'{"data": "test"}', properties, True)

    def _get_settings_mock(self) -> BunnySettings:
        return MagicMock(spec=BunnySettings, LOGGING={'LEVEL': logging.INFO,
                                                      'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                                      },)

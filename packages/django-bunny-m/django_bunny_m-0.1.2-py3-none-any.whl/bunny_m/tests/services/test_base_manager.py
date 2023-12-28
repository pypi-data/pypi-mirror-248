import logging
from unittest.mock import MagicMock

import pika
from django.test import TestCase

from bunny_m import BaseEvent
from bunny_m.services.base_manager import BaseManager
from bunny_m.settings import BunnySettings
from bunny_m.providers import ConnectionProvider


class BaseManagerTests(TestCase):
    def setUp(self) -> None:
        connection_provider_mock = MagicMock(spec=ConnectionProvider)
        connection_provider_mock.get_connection = MagicMock(return_value=MagicMock(spec=pika.BlockingConnection))
        settings_mock = self._get_settings_mock()
        self.base_manager = BaseManager(connection_provider=connection_provider_mock, bunny_settings=settings_mock)

    def test_init(self) -> None:
        self.base_manager.init()
        self.assertIsInstance(self.base_manager._connection, pika.BlockingConnection)
        self.assertIsNotNone(self.base_manager._channel)

    def test_create_exchange(self) -> None:
        channel_mock = MagicMock()
        channel_mock.exchange_declare = MagicMock()
        event_mock = MagicMock(spec=BaseEvent)
        event_mock.get_event_name = MagicMock(return_value="event_name")
        event_mock.EXCHANGE_TYPE = 2
        self.base_manager._channel = channel_mock
        self.base_manager.create_exchange(event_mock)
        channel_mock.exchange_declare.assert_called_with(event_mock.get_event_name(), exchange_type=event_mock.EXCHANGE_TYPE,
                                 internal=False, passive=False, durable=True, auto_delete=False)

        self.base_manager._channel = MagicMock()

    def test_close(self) -> None:
        channel_mock = MagicMock(is_open=True)
        channel_mock.close = MagicMock()
        self.base_manager._channel = channel_mock
        self.base_manager._connection = MagicMock(spec=pika.BlockingConnection, is_open=True)
        self.base_manager.close()
        self.base_manager._connection.close.assert_called()
        self.base_manager._channel.close.assert_called()

    def _get_settings_mock(self) -> BunnySettings:
        return MagicMock(spec=BunnySettings, LOGGING={'LEVEL': logging.INFO,
                                                      'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                                      },)

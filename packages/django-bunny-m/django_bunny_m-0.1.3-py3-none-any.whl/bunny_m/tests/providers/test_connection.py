from unittest.mock import patch, MagicMock

import pika
from django.test import TestCase

from bunny_m.settings import BunnySettings
from bunny_m.providers import ConnectionProvider


class ConsumerProviderTests(TestCase):
    @patch('pika.BlockingConnection')
    def test_get_connection(self, blocking_connection_mock) -> None:
        settings_mock = self._get_settings_mock()
        connection_provider = ConnectionProvider(settings_mock)
        connection_provider.get_connection()
        called_connection_params = blocking_connection_mock.call_args[0][0]
        self.assertIsInstance(called_connection_params, pika.ConnectionParameters)
        self.assertEqual(settings_mock.RABBIT_USER, called_connection_params.credentials.username)
        self.assertEqual(settings_mock.RABBIT_PASSWD, called_connection_params.credentials.password)
        self.assertIsNotNone(called_connection_params.ssl_options)
        self.assertEqual(settings_mock.RABBIT_HOST, called_connection_params.host)
        self.assertEqual(settings_mock.RABBIT_PORT, called_connection_params.port)
        self.assertEqual(settings_mock.RABBIT_VIRTUAL_HOST, called_connection_params.virtual_host)
        self.assertEqual(settings_mock.RABBIT_VIRTUAL_HOST, called_connection_params.virtual_host)
        self.assertEqual(settings_mock.RABBIT_CHANNEL_MAX, called_connection_params.channel_max)
        self.assertEqual(settings_mock.RABBIT_HEARTBEAT, called_connection_params.heartbeat)
        self.assertEqual(settings_mock.RABBIT_BLOCKING_TIMEOUT, called_connection_params.blocked_connection_timeout)

    def _get_settings_mock(self) -> BunnySettings:
        return MagicMock(spec=BunnySettings, RABBIT_USER='user', RABBIT_PASSWD='pass',
                                  RABBIT_USE_SSL=True, RABBIT_HOST='host.com', RABBIT_PORT=3333,
                                  RABBIT_VIRTUAL_HOST='/', RABBIT_CHANNEL_MAX=128, RABBIT_HEARTBEAT=60,
                                  RABBIT_BLOCKING_TIMEOUT=100)

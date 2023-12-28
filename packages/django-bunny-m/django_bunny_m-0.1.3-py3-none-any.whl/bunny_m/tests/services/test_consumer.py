import logging
from unittest.mock import MagicMock, patch

import pika
from django.db import OperationalError
from django.test import TestCase
from marshmallow import ValidationError
from pika.exceptions import AMQPChannelError, AMQPConnectionError

from bunny_m import BaseConsumer
from bunny_m.exceptions import NackException, RequeueException
from bunny_m.services import ConsumerManager
from bunny_m.settings import BunnySettings
from bunny_m.providers import ConnectionProvider


class ConsumerManagerTests(TestCase):
    EVENT_NAME = 'test_event'

    def setUp(self) -> None:
        handle = MagicMock()
        self.handle = handle
        self.basic_ack = MagicMock()
        self.basic_nack = MagicMock()
        self.basic_reject = MagicMock()
        channel = MagicMock()
        channel.basic_ack = self.basic_ack
        channel.basic_nack = self.basic_nack
        channel.basic_reject = self.basic_reject
        queue_mock = MagicMock()
        consumer_mock = MagicMock(spec=BaseConsumer)
        consumer_mock.handle = handle
        event_mock = MagicMock()
        event_mock.get_event_name = MagicMock(return_value=self.EVENT_NAME)
        consumer_mock.get_event_class = MagicMock(return_value=event_mock)
        channel.queue_declare = MagicMock(return_value=MagicMock(method=MagicMock(queue=queue_mock)))
        channel.queue_bind = MagicMock()
        channel.basic_consume = MagicMock(side_effect=lambda **params: params['on_message_callback'](channel,
                                                                                                     MagicMock(delivery_tag='TAG'),
                                                                                                     MagicMock(),
                                                                                                     MagicMock()))
        channel.basic_publish = MagicMock()
        connection_provider_mock = MagicMock(spec=ConnectionProvider)
        connection_mock = MagicMock(spec=pika.BlockingConnection)
        connection_mock.channel = MagicMock(return_value=channel)
        connection_provider_mock.get_connection = MagicMock(return_value=connection_mock)
        self.consumer = ConsumerManager(consumer_mock, bunny_settings=self._get_settings_mock(),
                                        connection_provider=connection_provider_mock)

        self.consumer._channel = channel
        self.queue_mock = queue_mock
        self.channel = channel

    def test_init(self) -> None:
        self.consumer.init()
        self.channel.queue_declare.assert_called_with('test__test_event', passive=False, durable=True, exclusive=False,
                                          auto_delete=False, arguments={'x-dead-letter-exchange': '',
                                                                        'x-dead-letter-routing-key': 'test__dead'})
        self.channel.queue_bind.assert_called_with(self.queue_mock, self.EVENT_NAME)

    def test_init_dead_queue(self) -> None:
        self.consumer.init_dead_queue()
        self.channel.queue_declare.assert_called_with('test__dead', passive=False,
                              durable=True, exclusive=False, auto_delete=False)

    @patch('simplejson.loads')
    def test_start_consume(self, json_mock) -> None:
        self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_ack.assert_called()

    @patch('simplejson.loads')
    def test_start_consume__nack_exception(self, json_mock) -> None:
        self.handle.side_effect = NackException
        self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_nack.assert_called_with(delivery_tag='TAG', requeue=False)

    @patch('simplejson.loads')
    def test_start_consume__requeue_exception(self, json_mock) -> None:
        self.handle.side_effect = RequeueException
        self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_nack.assert_called_with(delivery_tag='TAG', requeue=True)

    @patch('simplejson.loads')
    def test_start_consume__validation_exception(self, json_mock) -> None:
        self.handle.side_effect = ValidationError('test')
        self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_reject.assert_called_with(delivery_tag='TAG', requeue=False)

    @patch('simplejson.loads')
    def test_start_consume__operational_error(self, json_mock) -> None:
        self.handle.side_effect = OperationalError()
        with self.assertRaises(OperationalError):
            self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_reject.assert_called_with(delivery_tag='TAG', requeue=True)

    @patch('simplejson.loads')
    def test_start_consume__amqp_channel_error(self, json_mock) -> None:
        self.handle.side_effect = AMQPChannelError
        with self.assertRaises(AMQPChannelError):
            self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_reject.assert_called_with(delivery_tag='TAG', requeue=True)

    @patch('simplejson.loads')
    def test_start_consume__amqp_connection_error(self, json_mock) -> None:
        self.handle.side_effect = AMQPConnectionError
        with self.assertRaises(AMQPConnectionError):
            self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_reject.assert_called_with(delivery_tag='TAG', requeue=True)

    @patch('simplejson.loads')
    def test_start_consume__exception(self, json_mock) -> None:
        self.handle.side_effect = Exception
        with self.assertRaises(Exception):
            self.consumer.start_consume()
        self.handle.assert_called()
        self.basic_reject.assert_called_with(delivery_tag='TAG', requeue=False)


    def _get_settings_mock(self) -> BunnySettings:
        return MagicMock(spec=BunnySettings, APP_NAME='test', DEAD_LETTER_QUEUE_NAME='dead', LOGGING={'LEVEL': logging.INFO,
                                                      'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                                      }, )

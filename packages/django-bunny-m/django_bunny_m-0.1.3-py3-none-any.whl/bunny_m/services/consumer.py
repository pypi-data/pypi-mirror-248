from typing import Optional, Type

import simplejson as json
from django.db import OperationalError
from marshmallow import ValidationError
from pika.exceptions import AMQPChannelError, AMQPConnectionError
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import BasicProperties
from bunny_m import BaseEvent
from bunny_m.consumer import BaseConsumer, BaseDictConsumer
from bunny_m.exceptions import RequeueException, NackException
from bunny_m.providers.connection import ConnectionProvider
from bunny_m.services.base_manager import BaseManager
from bunny_m.settings import BunnySettings


class ConsumerManager(BaseManager):
    GLUE = '__'

    def __init__(self, consumer: Optional[BaseConsumer] = None,
                 connection_provider: Optional[ConnectionProvider] = None,
                 bunny_settings: Optional[BunnySettings] = None):
        super().__init__(connection_provider, bunny_settings)
        self._consumer = None
        self._event_class = None
        self._message_instance = None
        self._queue_name = None
        if consumer:
            self._consumer = consumer
            self._event_class = self._consumer.get_event_class()
            self._queue_name = self._get_queue_name(self._event_class)

    def init(self) -> None:
        super().init()
        if not self._consumer:
            return
        self.create_exchange(self._event_class)
        self._logger.info(f"Init queue {self._queue_name}")
        queue = self._channel.queue_declare(self._queue_name, passive=False, durable=True, exclusive=False,
                                          auto_delete=False, arguments={'x-dead-letter-exchange': '',
                                                                        'x-dead-letter-routing-key': self._get_dead_letter_queue_name()}).method.queue
        self._channel.queue_bind(queue, self._event_class.get_event_name())

    def init_dead_queue(self) -> None:
        dead_queue_name = self._get_dead_letter_queue_name()
        self._logger.info(f"Dead queue {dead_queue_name} initialization....")
        self._channel.queue_declare(dead_queue_name, passive=False,
                              durable=True, exclusive=False, auto_delete=False)

    def start_consume(self) -> None:
        self._channel.basic_qos()
        self._channel.basic_qos(prefetch_count=1)
        def callback(ch: BlockingChannel, method, properties: BasicProperties, body: bytes):
            try:
                body_str = body.decode('utf-8')
                self._logger.info(f"Gets message {body_str}")
                message = self._event_class.get_message_format().load(json.loads(body_str))
                self._consumer.handle(message)
                ch.basic_ack(method.delivery_tag)
            except NackException as e:
                self._logger.info(e)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            except RequeueException as e:
                self._logger.info(e)
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
            except ValidationError as e:
                self._logger.error(e)
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            except OperationalError as e:
                self._logger.error(e)
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
                raise e
            except AMQPChannelError as e:
                self._logger.error(e)
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
                raise e
            except AMQPConnectionError as e:
                self._logger.error(e)
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=True)
                raise e
            except Exception as e:
                self._logger.error(e)
                ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
                raise e
        self._channel.basic_consume(queue=self._queue_name, auto_ack=False, on_message_callback=callback)
        self._logger.info(f"Start consuming {self._queue_name}")
        self._channel.start_consuming()

    def _get_queue_name(self, event_class: Type[BaseEvent]) -> str:
        app_name = self._settings.APP_NAME
        event_name = event_class.get_event_name()
        return f'{app_name}{self.GLUE}{event_name}'

    def _get_dead_letter_queue_name(self) -> str:
        app_name = self._settings.APP_NAME
        dead_letter_name = self._settings.DEAD_LETTER_QUEUE_NAME
        return f'{app_name}{self.GLUE}{dead_letter_name}'

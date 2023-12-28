from typing import Optional, Type, Union

import pika
from typing import Callable
import simplejson as json
from pika import DeliveryMode

from bunny_m import BaseEvent
from bunny_m.message import Message
from bunny_m.providers import ConnectionProvider
from bunny_m.services.base_manager import BaseManager
from bunny_m.settings import BunnySettings


class ProducerManager(BaseManager):
    CONTENT_TYPE = 'text/json'

    def __init__(self, event_class: Type[BaseEvent], connection_provider: Optional[ConnectionProvider] = None,
                 bunny_settings: Optional[BunnySettings] = None,
                 delivery_callback: Optional[Callable]=None):
        super().__init__(connection_provider, bunny_settings)
        self._delivery_callback = delivery_callback
        self._is_mandatory = bool(self._delivery_callback)
        self._event_class = event_class

    def init(self) -> None:
        super().init()
        self.create_exchange(self._event_class)
        if self._delivery_callback:
            self._channel.confirm_delivery(callback=self._delivery_callback)

    def produce(self, message: Union[Message, dict]) -> None:
        exchange_name = self._event_class.get_event_name()
        message_dict = self._event_class.get_message_format().dump(message)
        message_json = json.dumps(message_dict)
        self._logger.info(f"produce {message_json} --- to {exchange_name}")
        self._channel.basic_publish(exchange_name, '', message_json.encode(encoding='UTF-8', errors='ignore'),
                pika.BasicProperties(content_type=self.CONTENT_TYPE, delivery_mode=DeliveryMode.Persistent), self._is_mandatory)

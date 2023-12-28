import logging
from typing import Optional, Type

from bunny_m import BaseEvent
from bunny_m.logger import DefaultLoggerConfigurator
from bunny_m.providers.connection import ConnectionProvider
from bunny_m.settings import BunnySettings


class BaseManager:
    def __init__(self, connection_provider: Optional[ConnectionProvider] = None,
                 bunny_settings: Optional[BunnySettings] = None):
        self._settings = bunny_settings or BunnySettings()
        self._connection_provider = connection_provider or ConnectionProvider(self._settings)
        self._set_logger()
        self._connection = None
        self._channel = None

    def init(self) -> None:
        self._connection = self._connection_provider.get_connection()
        self._channel = self._connection.channel()

    def create_exchange(self, event_class: Type[BaseEvent]) -> None:
        self._channel.exchange_declare(event_class.get_event_name(), exchange_type=event_class.EXCHANGE_TYPE,
                                 internal=False, passive=False, durable=True, auto_delete=False)

    def close(self) -> None:
        if self._channel and self._channel.is_open:
            self._channel.close()
        if self._connection and self._connection.is_open:
            self._connection.close()

    def _set_logger(self) -> None:
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            default_logger_configurator = DefaultLoggerConfigurator(self._settings)
            logger = default_logger_configurator.get_logger(__name__)
        self._logger = logger

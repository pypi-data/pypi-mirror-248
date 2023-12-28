import logging
from typing import Optional

from bunny_m.settings import BunnySettings


class DefaultLoggerConfigurator:
    def __init__(self, communicator_settings: Optional[BunnySettings] = None):
        if communicator_settings is None:
            communicator_settings = BunnySettings()
        self._communicator_settings = communicator_settings
        self._logging_level = self._communicator_settings.LOGGING['LEVEL']
        self._logging_format = self._communicator_settings.LOGGING['FORMAT']

    def get_logger(self, logger_name: str) -> logging.Logger:
        logger = logging.getLogger(logger_name)
        logger.setLevel(self._logging_level)
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(self._logging_format)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger

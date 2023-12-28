import logging
import copy
from typing import Optional

from django.conf import settings

BUNNY_M = 'BUNNY_M'

DEFAULTS = {
    'RABBIT_HOST': '127.0.0.1',
    'RABBIT_USER': 'guest',
    'RABBIT_PASSWD': 'guest',
    'RABBIT_BLOCKING_TIMEOUT': 300,
    'RABBIT_CHANNEL_MAX': 64,
    'RABBIT_PORT': 5672,
    'RABBIT_HEARTBEAT': 300,
    'RABBIT_VIRTUAL_HOST': '/',
    'DEAD_LETTER_QUEUE_NAME': 'dead_letter_queue',
    'RABBIT_USE_SSL': False,
    'LOGGING': {
        'LEVEL': logging.INFO,
        'FORMAT': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    },
    'CONSUMERS': []
}


class BunnySettings:
    def __init__(self, custom_settings: Optional[dict] = None):
        if custom_settings:
            self._user_settings = copy.deepcopy(custom_settings)
        else:
            self._user_settings = getattr(settings, BUNNY_M, {})
        self._defaults = DEFAULTS

    def __getattr__(self, attr):
        if (attr not in self._defaults) and (attr not in self._user_settings):
            raise AttributeError(f"Invalid setting: '{attr}'")
        return self._user_settings.get(attr, self._defaults.get(attr))

from pathlib import Path
from typing import Optional
import os

from django.conf import settings
from django.template.loader import render_to_string

from bunny_m.exceptions import EventAlreadyExistsException
from bunny_m.settings import BunnySettings


class Generator:
    MESSAGE_SUFFIX = 'Message'
    MESSAGE_FORMAT_SUFFIX = 'MessageFormat'
    EVENT_SUFFIX = 'Event'
    BASE_CONSUMER_SUFFIX = 'BaseConsumer'

    MESSAGES_PACKAGE = 'messages'
    MESSAGES_FORMAT_PACKAGE = 'messages/formats'
    EVENTS_PACKAGE = 'events'
    BASE_CONSUMERS_PACKAGE = 'consumers'

    PACKAGES = {MESSAGES_PACKAGE: MESSAGE_SUFFIX, MESSAGES_FORMAT_PACKAGE: MESSAGE_FORMAT_SUFFIX,
                EVENTS_PACKAGE: EVENT_SUFFIX, BASE_CONSUMERS_PACKAGE: BASE_CONSUMER_SUFFIX}

    PACKAGE_INIT = '__init__.py'

    def __init__(self, event_name: str, settings_provider: Optional[BunnySettings] = None):
        self._event_name = event_name
        self._settings_provider = settings_provider or BunnySettings()

    def _get_path(self) -> str:
        pass

    def init_packages(self) -> None:
        for package, class_suffix in self.PACKAGES.items():
            path = os.path.join(settings.BASE_DIR, self._settings_provider.MESSAGE_DIR, package)
            Path(path).mkdir(parents=True, exist_ok=True)
            with open(os.path.join(path, self.PACKAGE_INIT), "a", encoding="utf-8") as init_file:
                class_name = self._get_class_name(class_suffix)
                init_file.write(f"from .{self._event_name} import {class_name}\n")

    def create_message(self) -> None:
        body = render_to_string('message_template.py', {'message_class_name': self._get_class_name(self.MESSAGE_SUFFIX)})
        with open(self.get_message_path(), "w", encoding="utf-8") as f:
            f.write(body)

    def create_message_format(self) -> None:
        body = render_to_string('message_format_template.py', {
            'message_class_location': self._get_class_path(self.MESSAGES_PACKAGE),
            'message_class_name': self._get_class_name(self.MESSAGE_SUFFIX),
            'message_format_class_name': self._get_class_name(self.MESSAGE_FORMAT_SUFFIX),
        })
        with open(self.get_message_format_path(), "w", encoding="utf-8") as f:
            f.write(body)

    def create_event(self) -> None:
        body = render_to_string('event_template.py', {
            'message_format_class_location': self._get_class_path(self.MESSAGES_FORMAT_PACKAGE),
            'event_class_name': self._get_class_name(self.EVENT_SUFFIX),
            'message_format_class_name': self._get_class_name(self.MESSAGE_FORMAT_SUFFIX),
            'event_name': self._event_name,

        })
        with open(self.get_event_path(), "w", encoding="utf-8") as f:
            f.write(body)

    def create_base_consumer(self) ->  None:
        body = render_to_string('base_consumer_template.py', {
            'event_class_location': self._get_class_path(self.EVENTS_PACKAGE),
            'event_class_name': self._get_class_name(self.EVENT_SUFFIX),
            'message_class_location': self._get_class_path(self.MESSAGES_PACKAGE),
            'message_class_name': self._get_class_name(self.MESSAGE_SUFFIX),
            'base_consumer_class_name':  self._get_class_name(self.BASE_CONSUMER_SUFFIX),
        })
        with open(self.get_base_consumer_path(), "w", encoding="utf-8") as f:
            f.write(body)

    def get_message_path(self) -> str:
        return os.path.join(settings.BASE_DIR, self._settings_provider.MESSAGE_DIR,
                            self.MESSAGES_PACKAGE, self._event_name + '.py')

    def get_message_format_path(self) -> str:
        return os.path.join(settings.BASE_DIR, self._settings_provider.MESSAGE_DIR,
                            self.MESSAGES_FORMAT_PACKAGE, self._event_name + '.py')

    def get_event_path(self) -> str:
        return os.path.join(settings.BASE_DIR, self._settings_provider.MESSAGE_DIR,
                            self.EVENTS_PACKAGE, self._event_name + '.py')

    def get_base_consumer_path(self) -> str:
        return os.path.join(settings.BASE_DIR, self._settings_provider.MESSAGE_DIR,
                            self.BASE_CONSUMERS_PACKAGE, self._event_name + '.py')

    def check_event(self, path: str) -> None:
        if os.path.exists(path):
            raise EventAlreadyExistsException(f"Event {self._event_name} already exists")

    def _get_class_path(self, package_path: str) -> str:
        path = os.path.join(self._settings_provider.MESSAGE_DIR, package_path, self._event_name)
        return path.replace(os.sep, '.')

    def _get_class_name(self, suffix: str) -> str:
        return ''.join([ele.title() for ele in self._event_name.split('_')]) + suffix

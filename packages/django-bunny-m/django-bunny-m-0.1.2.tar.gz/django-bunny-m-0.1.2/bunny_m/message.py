from typing import Type, Optional

from marshmallow import Schema, post_load


class Message:
    pass


class BaseMessageFormat(Schema):
    @classmethod
    def get_message_class(cls) -> Optional[Type[Message]]:
        return None

    @post_load
    def make_message(self, data, **kwargs) -> Message:
        message_class = self.get_message_class()
        if message_class:
            return message_class(**data)
        return data


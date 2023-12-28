from typing import Optional, Type

from bunny_m import BaseMessageFormat, Message

from {{ message_class_location }} import {{ message_class_name }}


class {{ message_format_class_name }}(BaseMessageFormat):
    #Add your validation here

    @classmethod
    def get_message_class(cls) -> Optional[Type[Message]]:
        return {{message_class_name}}

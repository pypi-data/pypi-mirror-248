from bunny_m import BaseEvent

from {{message_format_class_location}} import {{ message_format_class_name }}


class {{ event_class_name }}(BaseEvent):
    @classmethod
    def get_event_name(cls) -> str:
        return '{{ event_name }}'

    @classmethod
    def get_message_format(cls) -> {{ message_format_class_name }}:
        return {{ message_format_class_name }}()

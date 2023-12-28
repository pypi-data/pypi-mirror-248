========================
Bunny M (Bunny Message)
========================

Bunny M is a Django module that allows you to easily create communication
using RabbitMQ. Particularly useful when creating a microservice ecosystem


Quick start
------------
1. Install bunny_m module by command::

    pip install django-bunny-m

1. Add "bunny_m" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "bunny_m",
    ]

Configuration
--------------
Minimal configuration to set in project settings.py file::

    BUNNY_M = {
        'APP_NAME': 'TEST_APP',
        'MESSAGE_DIR': 'bands/communication',
        'CONSUMERS': [
            'bands.consumers.AlbumUpdateConsumer',
            'bands.consumers.BandUpdateConsumer',
            'bands.consumers.ConcertUpdateConsumer',
        ]
    }

APP_NAME
    Application name. Used to generate RabbitMQ queue names
MESSAGE_DIR
    Path for automatic events files generator
CONSUMERS
    List of consumer class paths

All default configuration options
-----------------------------------

All preconfigured options::

    BUNNY_M = {
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


Automatic event files generator
--------------------------------

Bunny_m module has built-in command which supports events addition

1. Run command::

    python manage.py create_bunny_event --event_name=<YOUR_EVENT_NAME>


(Use _ separated event name like: `product_update`, `manufacturer_update`, `manufacturer_delete` etc..


2. Predefined files was automatically created in structure located in ``MESSAGE_DIR`` path


Message
--------
Messages are located in ``<MESSAGE_DIR>/messages/<event_name>.py``
Messages are dataclasses which represents RabbitMQ message domain::

    from dataclasses import dataclass

    from bunny_m import Message


    @dataclass
    class BandUpdateMessage(Message):
        name: str
        email: str
        site: str


Message format
----------------
Message formats are located in ``<MESSAGE_DIR>/messages/formats/<event_name>.py``
Classes are based on marshmallow Schema: https://marshmallow.readthedocs.io/en/stable/
and supports message validation and serialization/deserialization::

    from typing import Optional, Type

    from bunny_m import BaseMessageFormat, Message
    from marshmallow import fields

    from bands.communication.messages.band_update import BandUpdateMessage


    class BandUpdateMessageFormat(BaseMessageFormat):
        name = fields.Str()
        email = fields.Email()
        site = fields.Url()

        @classmethod
        def get_message_class(cls) -> Optional[Type[Message]]:
            return BandUpdateMessage


Event
-------
Located in ``<MESSAGE_DIR>/events/<event_name>.py``
Events classes are RabbitMQ exchangers representation. They are fully automatically generated - You don't need change anything::

    from bunny_m import BaseEvent

    from bands.communication.messages.formats.band_update import BandUpdateMessageFormat


    class BandUpdateEvent(BaseEvent):
        @classmethod
        def get_event_name(cls) -> str:
            return 'band_update'

        @classmethod
        def get_message_format(cls) -> BandUpdateMessageFormat:
            return BandUpdateMessageFormat()


Base Consumer
--------------
Located in Located in ``<MESSAGE_DIR>/consumers/<event_name>.py``
Like events, Consumers are automatically generated. You need ony implement `handle` method::

    from abc import ABC, abstractmethod
    from typing import Type

    from bunny_m import BaseEvent, BaseConsumer

    from bands.communication.events.band_update import BandUpdateEvent
    from bands.communication.messages.band_update import BandUpdateMessage


    class BandUpdateBaseConsumer(BaseConsumer, ABC):
        @classmethod
        def get_event_class(cls) -> Type[BaseEvent]:
            return BandUpdateEvent

        @abstractmethod
        def handle(self, message: BandUpdateMessage) -> None:
            pass

Simple consumer implementation
---------------------------------
Here is simple consumer implementation which can be added to ``CONSUMERS`` setting::

    import time

    from bands.communication.consumers import BandUpdateBaseConsumer
    from bands.communication.messages import BandUpdateMessage


    class BandUpdateConsumer(BandUpdateBaseConsumer):
        def handle(self, message: BandUpdateMessage) -> None:
            print(f"BandUpdateEventConsumer - I'am get {message.name} band")
            time.sleep(1)


Run consuming
--------------
Bunny_m has special prepared script which run all registered consumers in separated processes.
Each fail of consumer are logged and cause consumer process restart::

    python manage.py start_all_consumers


Simple publishing events
-------------------------
Here is a example of simple BandMessage event producer::

        bands_producer = ProducerManager(BandUpdateEvent)
        bands_producer.init()
        band_message = BandUpdateMessage(name='T.a.t.U', email='tatu@yandex.ru', site='http://www.tatu.ru')
        bands_producer.produce(band_message)
        bands_producer.close()

Consumer life cycle
--------------------
Consumers are long-lived programs that may experience various exceptions during their operation, such as breaking the connection to the database or the connection to RabbitMQ.
During such an error, the message is requeued and the script is automatically restarted

You can decide about the message while handling it by throwing appropriate exceptions

NackException
    send `nack` to RabbitMQ and remove message from queue

RequeueException
    send `reject` to RabbitMQ and requeue the message

MQPConnectionError, OperationalError
    send `reject` to RabbitMQ and requeue the message and restart consumer

Exception based
    send `reject` to RabbitMQ and redirect message to a dead-queue


Example project
----------------

Example project are available here: https://github.com/Zwiezda/bunny_m_example

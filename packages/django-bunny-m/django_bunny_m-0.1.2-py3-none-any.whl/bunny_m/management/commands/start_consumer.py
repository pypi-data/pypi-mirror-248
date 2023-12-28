import sys
from pika.exceptions import AMQPConnectionError
from django.core.management import BaseCommand

from bunny_m.logger import DefaultLoggerConfigurator
from bunny_m.providers import ConsumersProvider
from bunny_m.services.consumer import ConsumerManager
from bunny_m.settings import BunnySettings


class Command(BaseCommand):
    PATH_CONSUMER_CLASSPATH = 'consumer_classpath'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self._settings = BunnySettings()
        self._consumers_provider = ConsumersProvider()
        self._logger = DefaultLoggerConfigurator(self._settings).get_logger(__name__)
        self._consumer_classpath = None

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument(
            f"--{self.PATH_CONSUMER_CLASSPATH}",
            help="Consumer classpath",
        )

    def handle(self, *args, **options) -> None:  # pragma: no cover
        self._consumer_classpath = options.get(self.PATH_CONSUMER_CLASSPATH)
        if not self._consumer_classpath:
            self._logger.error(f"Classpath is not set")
            return
        self._logger.info(f"{self._consumer_classpath} starting....")
        consumer_manager = None
        try:
            consumer = self._consumers_provider.get_consumer_instance(self._consumer_classpath)
            consumer_manager = ConsumerManager(consumer)
            consumer_manager.init()
            consumer_manager.start_consume()
        except AMQPConnectionError as e:
            self._logger.error(e)
            sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)
        finally:
            self._logger.info(f'{self._consumer_classpath} stopping....')
            if consumer_manager:
                consumer_manager.close()

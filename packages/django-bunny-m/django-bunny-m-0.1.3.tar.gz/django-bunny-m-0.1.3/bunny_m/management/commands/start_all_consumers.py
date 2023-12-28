import multiprocessing
import os
import queue
import signal
import sys
from time import sleep
from typing import Dict

from django.core.management import BaseCommand

from bunny_m.logger import DefaultLoggerConfigurator

from bunny_m.services import ConsumerManager
from bunny_m.settings import BunnySettings


def run_queue_consumer(consumer_classpath: str) -> None:
    os.execlp('python', 'python', 'manage.py', 'start_consumer', f'--consumer_classpath={consumer_classpath}')


class Command(BaseCommand):
    PATH_CONSUMER_CLASSPATH = 'consumer_classpath'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self._settings = BunnySettings()
        self._logger = DefaultLoggerConfigurator().get_logger(__name__)
        self._processes: Dict[str, multiprocessing.Process] = {}
        self._consumer_manager = ConsumerManager()

    def handle(self, *args, **options) -> None:  # pragma: no cover
        signal.signal(signal.SIGINT, self.handle_sigint)
        self._logger.info(f"Main consumer starting....")
        try:
            self._consumer_manager.init()
            self._consumer_manager.init_dead_queue()
        except Exception as e:
            self._logger.exception(e)
            sys.exit(1)
        finally:
            self._consumer_manager.close()
        if not self._settings.CONSUMERS:
            self._logger.info(f"No registered consumers. Shutting down....")
            sys.exit(1)
        for consumer_classpath in self._settings.CONSUMERS:
            self._processes[consumer_classpath] = self._start_process(consumer_classpath)
        try:
            while True:
                sleep(10)
                for consumer_classpath, process in self._processes.items():
                    if not process.is_alive():
                        self._logger.info(f"{consumer_classpath} is dead. Restart...")
                        self._processes[consumer_classpath] = self._start_process(consumer_classpath)
        except KeyboardInterrupt:
            self.handle_sigint(None, None)

    def _start_process(self, consumer_classpath: str) -> multiprocessing.Process:
        process = multiprocessing.Process(target=run_queue_consumer, args=(consumer_classpath,))
        process.start()
        return process

    def handle_sigint(self, signum, frame):
        self._logger.info('Counsumers stopping....')
        for process in self._processes.values():
            process.kill()
        sys.exit(0)

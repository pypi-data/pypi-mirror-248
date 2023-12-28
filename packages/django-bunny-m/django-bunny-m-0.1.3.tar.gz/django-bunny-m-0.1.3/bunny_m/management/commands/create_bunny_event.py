from django.core.management import BaseCommand

from bunny_m.exceptions import EventAlreadyExistsException
from bunny_m.generator import Generator


class Command(BaseCommand):
    EVENT_NAME_ARG = 'event_name'

    def add_arguments(self, parser):  # pragma: no cover
        parser.add_argument(
            f"--{self.EVENT_NAME_ARG}",
            help="Event name",
        )

    def handle(self, *args, **options) -> None:  # pragma: no cover
        event_name = options.get(self.EVENT_NAME_ARG)
        if not event_name:
            self.stderr.write(f"Arg event_name is required!")
            return
        generator = Generator(event_name)
        try:
            generator.check_event(generator.get_event_path())
        except EventAlreadyExistsException as e:
            self.stderr.write(str(e))
            return
        generator.init_packages()
        self.stdout.write(f"Creating {generator.get_message_path()}", ending='\n')
        generator.create_message()
        self.stdout.write(f"Creating {generator.get_message_format_path()}", ending='\n')
        generator.create_message_format()
        self.stdout.write(f"Creating {generator.get_event_path()}", ending='\n')
        generator.create_event()
        self.stdout.write(f"Creating {generator.get_base_consumer_path()}", ending='\n')
        generator.create_base_consumer()

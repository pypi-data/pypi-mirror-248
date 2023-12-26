import abc
import asyncio
import sys
from argparse import ArgumentParser, ArgumentError
from typing import Optional

from compito.scheduler import Scheduler


class Command:
    command_name: str
    scheduler: Optional[Scheduler] = None
    help_text: str = ''

    @abc.abstractmethod
    def handle(self, *args, **kwargs) -> None:
        pass

    def create_parser(self, **kwargs):
        parser = ArgumentParser(
            prog=f'{self.command_name}',
            description=self.help_text or None,
            **kwargs
        )
        self.add_arguments(parser)
        return parser

    def execute(self, *args, **kwargs):
        self.handle(*args, **kwargs)

    def add_arguments(self, parser):
        """
        Entry point for subclassed commands to add custom arguments.
        """
        pass

    def run_from_argv(self, argv):
        parser = self.create_parser()

        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop("args", ())
        try:
            self.execute(*args, **cmd_options)
        except ArgumentError as e:
            if options.traceback:
                raise

            sys.stderr.write("%s: %s" % (e.__class__.__name__, e))
            sys.exit(1)


class AsyncCommand(Command):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()

    async def handle(self, *args, **kwargs) -> None:
        pass

    def execute(self, *args, **kwargs):
        self.loop.run_until_complete(self.handle(*args, **kwargs))

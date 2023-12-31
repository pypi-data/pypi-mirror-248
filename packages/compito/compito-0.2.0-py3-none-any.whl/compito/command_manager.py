import os
import sys
from argparse import ArgumentParser
from difflib import get_close_matches

from compito.schedule_manager import ScheduleManager
from compito.utils import get_commands


class CommandManager:

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.command_name = os.path.basename(self.argv[0])
        if self.command_name == "__main__.py":
            self.command_name = "python -m compito"

    def fetch_command(self, subcommand):
        commands = get_commands()
        try:
            app_name = commands[subcommand]
        except KeyError:
            possible_matches = get_close_matches(subcommand, commands)
            sys.stderr.write("Unknown command: %r" % subcommand)
            if possible_matches:
                sys.stderr.write(". Did you mean %s?" % possible_matches[0])
            sys.stderr.write("\nType '%s help' for usage.\n" % self.command_name)
            sys.exit(1)
        return app_name()

    def main_help_text(self, commands_only=False):
        """Return the script's main help text, as a string."""
        if commands_only:
            usage = sorted(get_commands())
        else:
            usage = [
                "",
                "Type '%s <subcommand> --help' for help on a specific subcommand."
                % self.command_name,
                "",
                "Available subcommands:",
            ]
            for name, command in get_commands().items():
                usage.append("[%s]" % name)
                help_text = command().create_parser().format_help().split('\n')
                for line in help_text:
                    line = '   ' + line
                    usage.append(line)
        return "\n".join(usage)

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = "help"  # Display help if no arguments were given.

        parser = ArgumentParser(
            prog=self.command_name,
            usage="%(prog)s subcommand [options] [args]",
            add_help=False,
            allow_abbrev=False,
        )
        parser.add_argument("args", nargs="*")  # catch-all

        if subcommand == "help":
            sys.stdout.write(self.main_help_text() + "\n")
        elif subcommand == "schedule":
            ScheduleManager().start_scheduled_commands()
        else:
            self.fetch_command(subcommand).run_from_argv(self.argv)


def execute_from_command_line(argv=None):
    utility = CommandManager(argv)
    utility.execute()

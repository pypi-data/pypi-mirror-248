import functools
import importlib
import inspect
import os
import sys
import traceback
from typing import Dict, Type

from compito.command import Command, AsyncCommand


@functools.lru_cache(maxsize=None)
def get_commands(start_path: str = os.getcwd()) -> Dict[str, Type[Command]]:
    commands = {}

    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if not d.startswith('_')]
        for file in files:
            if not file.endswith(".py") and not file.startswith("_"):
                continue
            module_name = os.path.splitext(
                os.path.relpath(os.path.join(root, file), start_path).replace(os.sep, '.')
            )[0]
            try:
                module =  importlib.import_module(module_name)
            except Exception:
                sys.stderr.write(f"Error importing module {module_name}")
                sys.stderr.write(f"Traceback: {traceback.format_exc()}")
                continue

            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Command) and obj != Command and obj != AsyncCommand:
                    commands[obj.command_name] = obj

    return commands

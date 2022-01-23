"""Library to communicate with a Thinking Cleaner module asynchronously"""

import inspect
import sys
from distutils.cmd import Command

from aiothinkingcleaner.command_base import TCCommand

if sys.version_info >= (3, 8):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

from . import commands
from .thinkingcleaner import ThinkingCleaner


def get_version() -> str:
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "unknown"


version: str = get_version()

__all__ = ["ThinkingCleaner"]

for name, cls in inspect.getmembers(commands, inspect.isclass):
    if (
        issubclass(cls, TCCommand)
        and cls is not TCCommand
        and not name.startswith("_")
    ):
        ThinkingCleaner.register_command(cls())

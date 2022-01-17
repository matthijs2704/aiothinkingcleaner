"""Class for control of a Thinking Cleaner module"""

from .connection import ThinkingCleanerConnection
from .data import TCDeviceStatus


class ThinkingCleaner(ThinkingCleanerConnection):
    """Class representing a Thinking Cleaner module"""

    _registered_commands = {}

    @classmethod
    def register_command(cls, command):
        cls._registered_commands[command.name] = command
        setattr(cls, command.name, command)

    async def get_status(self) -> TCDeviceStatus:
        status = await self._get_status()
        return status

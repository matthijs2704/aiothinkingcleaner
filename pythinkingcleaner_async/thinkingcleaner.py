"""Class for control of a Thinking Cleaner module"""

from pythinkingcleaner_async.connection import ThinkingCleanerConnection
from pythinkingcleaner_async.data import TCCommand, TCDeviceStatus


class ThinkingCleaner(ThinkingCleanerConnection):
    """Class representing a Thinking Cleaner module"""

    async def get_status(self) -> TCDeviceStatus:
        status = await self._get_status()
        return status

    async def spot_clean(self) -> None:
        """Start spot cleaning."""
        return await self.send_command(TCCommand.SPOT)

    async def clean(self) -> None:
        """Start a normal cleaning cycle."""
        return await self.send_command(TCCommand.CLEAN)

    async def max_clean(self) -> None:
        """Start max cleaning, to keep cleaning until the battery runs low."""
        return await self.send_command(TCCommand.MAX)

    async def delayed_clean(self) -> None:
        """Start delayed cleaning."""
        return await self.send_command(TCCommand.DELAYED_CLEAN)

    async def dock(self) -> None:
        """Return to homebase immediately."""
        return await self.send_command(TCCommand.DOCK)

    async def find_me(self) -> None:
        """Play a sound to find Roomba."""
        return await self.send_command(TCCommand.FIND_ME)

    async def exit_dock(self) -> None:
        """Leave the dock and turn around 180 degrees."""
        return await self.send_command(TCCommand.EXIT_DOCK)

    async def power_off(self) -> None:
        """Turn Roomba off."""
        return await self.send_command(TCCommand.POWER_OFF)

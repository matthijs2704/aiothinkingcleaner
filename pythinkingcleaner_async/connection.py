"""Class representing the connection to the Thinking Cleaner module."""

import asyncio
from functools import partial

import aiohttp

from pythinkingcleaner_async.data import TCCommand
from pythinkingcleaner_async.exceptions import TCCommandFailed, TCErrorResponse


class ThinkingCleanerConnection:
    """Class representing a raw connection to Thinking Cleaner."""

    session = None
    """HTTP session used for API"""

    def __init__(self, target, timeout=60, verbose=False) -> None:
        """Create a new instance."""
        self.target = target

        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = aiohttp.ClientSession(
            f"http://{target}", timeout=self.timeout
        )

        self.verbose = (
            partial(print, self.target) if verbose is True else verbose
        )
        pass

    async def _get_status(self) -> dict:
        """Retreive the current status of the vacuum.

        Returns:
            dict: raw status response
        """
        async with self.session.get("/status.json") as resp:
            status_data = await resp.json(content_type=None)

            if self.verbose:
                self.verbose(status_data)

            if status_data["result"] == "success":
                return status_data["status"]

            raise TCErrorResponse

    async def send_command(self, command: TCCommand) -> None:
        """Send a command to the vacuum.

        Args:
            command (TCCommand): Command to send.
        """
        async with self.session.get(
            f"/command.json?command={command.value}"
        ) as cmd_resp:
            cmd_resp_data = await cmd_resp.json(content_type=None)

            if cmd_resp_data["result"] != "success":
                raise TCCommandFailed

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        if not self.session.closed:
            await self.session.close()

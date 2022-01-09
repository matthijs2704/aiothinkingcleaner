"""Class representing the connection to the Thinking Cleaner module."""

from typing import Any, Dict, Union

import asyncio
from functools import partial

import aiohttp

from pythinkingcleaner_async.data import TCCommand, TCDeviceStatus
from pythinkingcleaner_async.exceptions import TCCommandFailed, TCErrorResponse


class ThinkingCleanerConnection:
    """Class representing a raw connection to Thinking Cleaner."""

    session: aiohttp.ClientSession
    """HTTP session used for API"""

    def __init__(
        self, target: str, timeout: int = 60, verbose: bool = False
    ) -> None:
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

    async def _get_status(self) -> TCDeviceStatus:
        """Retreive the current status of the vacuum.

        Returns:
            dict: raw status response

        Raises:
            TCErrorResponse: when an error response is received from the device
        """
        async with self.session.get("/status.json") as resp:
            status_data = await resp.json(content_type=None)

            if self.verbose:
                self.verbose(status_data)  # type: ignore

            if status_data["result"] == "success":

                # ignore schedule serial number
                del status_data["status"]["schedule_serial_number"]

                status = TCDeviceStatus(**status_data["status"])
                return status

            raise TCErrorResponse

    async def send_command(self, command: TCCommand) -> None:
        """Send a command to the vacuum.

        Args:
            command (TCCommand): Command to send.

        Raises:
            TCCommandFailed: when a command does not exist or failed to execute
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

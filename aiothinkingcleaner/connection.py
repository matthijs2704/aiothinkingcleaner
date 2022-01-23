"""Class representing the connection to the Thinking Cleaner module."""

from typing import Any, Dict, Union

import asyncio
from functools import partial

import aiohttp

from aiothinkingcleaner.command_base import TCEndpoint

from .data import TCDeviceStatus
from .exceptions import TCCommandFailed, TCErrorResponse


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

    async def send(
        self, endpoint: TCEndpoint, command: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a command to the vacuum.

        Args:
            endpoint (TCEndpoint): Which endpoint to send the command to.
            command (str): Command to send.
            data (dict): Additional parameters for the command.

        Returns:
            dict: json return data of the command

        Raises:
            TCCommandFailed: when a command does not exist or failed to execute
        """

        data = data if data is not None else {}
        data["command"] = command

        async with self.session.get(
            f"/{endpoint.value}.json", params=data
        ) as cmd_resp:
            cmd_resp_data: Dict[str, Any] = await cmd_resp.json(
                content_type=None
            )

            if cmd_resp_data["result"] != "success":
                raise TCCommandFailed
            return cmd_resp_data

    # async def send_command(self, command: TCCommand) -> None:
    #     """Send a command to the vacuum.

    #     Args:
    #         command (TCCommand): Command to send.

    #     Raises:
    #         TCCommandFailed: when a command does not exist or failed to execute
    #     """
    #     async with self.session.get(
    #         f"/command.json?command={command.value}"
    #     ) as cmd_resp:
    #         cmd_resp_data = await cmd_resp.json(content_type=None)

    #         if cmd_resp_data["result"] != "success":
    #             raise TCCommandFailed

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        if not self.session.closed:
            await self.session.close()

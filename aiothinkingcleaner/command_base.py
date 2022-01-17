from enum import Enum
from functools import partial, partialmethod


class TCReturnData:
    # todo, what should it define
    pass


class TCEndpoint(Enum):
    """Type of command endpoint (json name)."""

    COMMAND = "command"
    REGISTER_WEBHOOK = "register_webhook"
    NEW_SONG = "new_song"


class TCCommandMeta(type):
    def __new__(mcs, name, bases, dict):
        if name.startswith("_") or name == "Command":
            return type.__new__(mcs, name, bases, dict)

        if "name" not in dict:
            dict["name"] = name.lower()

        cls = type.__new__(mcs, name, bases, dict)

        cls.__call__ = partialmethod(cls.__call__, data={})
        # if cls.GET:
        #     cls.__call__.__defaults__ = (b'',)
        # if not cls.SET or not cls.DATA:
        #     cls.__call__ = partialmethod(cls.__call__, data=b'')

        return cls


class TCCommand(metaclass=TCCommandMeta):
    # Endpoint type
    ENDPOINT: TCEndpoint = None

    # Str command name
    CMD: str = None

    # Str command name
    RETURN_DATA: TCReturnData = None

    async def __call__(self, connection, data: dict = {}) -> None:
        await connection.send_command(self.ENDPOINT, self.CMD, data)

    def __get__(self, connection, cls):
        if connection is None:
            return self  # bind to class
        return partial(self, connection)  # bind to instance

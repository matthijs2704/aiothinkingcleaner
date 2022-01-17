from enum import Enum
from functools import partial, partialmethod

from .exceptions import TCInvalidReturnType


class TCReturnData:
    # todo, what should it define
    pass


class TCEndpoint(Enum):
    """Type of command endpoint (json name)."""

    COMMAND = "command"
    REGISTER_WEBHOOK = "register_webhook"
    NEW_SONG = "new_song"
    STATUS = "status"
    FULL_STATUS = "full_status"


class TCCommandMeta(type):
    def __new__(mcs, name, bases, dict):
        if name.startswith("_") or name == "Command":
            return type.__new__(mcs, name, bases, dict)

        if "name" not in dict:
            dict["name"] = name.lower()

        if "DATA" not in dict and bases:
            # allow naive DATA inheritance
            dict["DATA"] = bases[0].DATA

        cls = type.__new__(mcs, name, bases, dict)

        cls.__call__.__defaults__ = (b"",)
        if not cls.DATA:
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

    # List of additional parameters to add
    DATA = {}

    # Str command name
    RETURNS = None

    async def __call__(self, connection, data) -> None:
        data = self.pack_params(data if data is not None else {})
        rtndata = await connection.send(self.ENDPOINT, self.CMD, data)
        if rtndata and self.RETURNS:
            if issubclass(self.RETURNS, TCReturnData):
                try:
                    return self.RETURNS(**rtndata[self.CMD])
                except TypeError as exc:
                    raise TCInvalidReturnType from exc
            else:
                raise TCInvalidReturnType

    def __get__(self, connection, cls):
        if connection is None:
            return self  # bind to class
        return partial(self, connection)  # bind to instance

    @classmethod
    def pack_params(cls, data):
        rd = {}
        for i, (fieldName, field) in enumerate(cls.DATA.items()):
            if isinstance(data[i], field):
                rd[fieldName] = data[i]
            else:
                raise ValueError("Missing mandatory data")
        return rd

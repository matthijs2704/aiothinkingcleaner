from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar

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


T = TypeVar("T", bound="TCCommandMeta")


class TCCommandMeta(type):
    ENDPOINT: TCEndpoint
    CMD: str
    DATA: Dict[str, Any]
    RETURNS: Optional[Type[TCReturnData]]

    def __new__(
        mcs: Type[T],
        name: str,
        bases: Tuple[type, ...],
        dict: Dict[str, Any],
    ) -> T:
        if name.startswith("_") or name == "TCCommand":
            return super().__new__(mcs, name, bases, dict)

        if "name" not in dict:
            dict["name"] = name.lower()

        if (
            "DATA" not in dict
            and len(bases) > 0
            and issubclass(bases[0], TCCommand)
        ):
            # allow naive DATA inheritance
            dict["DATA"] = bases[0].DATA

        cls = super().__new__(mcs, name, bases, dict)

        if not cls.DATA:
            cls.__call__ = partialmethod(cls.__call__, data={})  # type: ignore
        # if cls.GET:
        #     cls.__call__.__defaults__ = (b'',)
        # if not cls.SET or not cls.DATA:
        #     cls.__call__ = partialmethod(cls.__call__, data=b'')

        return cls


U = TypeVar("U")
V = TypeVar("V", bound="TCCommand")


class TCCommand(metaclass=TCCommandMeta):
    # Endpoint type
    ENDPOINT: TCEndpoint = TCEndpoint.COMMAND

    # Str command name
    CMD: str = ""

    # List of additional parameters to add
    DATA: Optional[Dict[str, Any]] = None

    # Str command name
    RETURNS: Optional[Type[TCReturnData]] = None

    async def __call__(
        self: V, connection: U, data: List[Any]
    ) -> Optional[Type[TCReturnData]]:
        dataDict = self.pack_params(data if data is not None else {})
        rtndata = await connection.send(self.ENDPOINT, self.CMD, dataDict)  # type: ignore
        if rtndata and self.RETURNS:
            if issubclass(self.RETURNS, TCReturnData):
                try:
                    return self.RETURNS(**rtndata[self.CMD])  # type: ignore
                except (KeyError, TypeError) as exc:
                    raise TCInvalidReturnType from exc
            else:
                raise TCInvalidReturnType
        else:
            return None

    def __get__(self: V, connection: Optional[U], cls: Type[type]):  # type: ignore
        if connection is None:
            return self  # bind to class
        return partial(self, connection)  # bind to instance

    @classmethod
    def pack_params(cls, data: List[Any]) -> Dict[str, Any]:
        rd = {}
        for i, (fieldName, field) in enumerate(cls.DATA.items()):
            if i < len(data) and isinstance(data[i], field):
                rd[fieldName] = data[i]
            else:
                raise ValueError("Missing mandatory data")
        return rd

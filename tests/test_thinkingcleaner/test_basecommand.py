from typing import Any, Dict

import enum
import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from aiothinkingcleaner.command_base import (
    TCCommand,
    TCCommandMeta,
    TCEndpoint,
    TCReturnData,
)
from aiothinkingcleaner.exceptions import *


class TCConnectionStub:
    def __init__(
        self, result_success: bool = True, bad_response: bool = False
    ) -> None:
        self.result_success = result_success
        self.bad_response = bad_response
        pass

    async def send(
        self, endpoint: TCEndpoint, command: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        if self.bad_response:
            return {"data": "bad"}

        return {
            command: {
                "endpoint": endpoint,
                "action": command,
                "result": "success" if self.result_success else "failed",
                "data": data,
            }
        }


class DummyCommand(metaclass=TCCommandMeta):
    ENDPOINT = "test"
    CMD = "test_cmd"
    DATA = {"testParam": str}

    pass


class BaseCommandTests(unittest.TestCase):
    def test_meta_inherit(self):
        test_obj = DummyCommand()
        assert (test_obj.name) == "dummycommand"
        assert (test_obj.ENDPOINT) == "test"
        assert (test_obj.DATA) == {"testParam": str}
        assert (test_obj.CMD) == "test_cmd"

    def test_meta_data(self):
        test_obj = DummyCommand()
        test_obj.DATA = {"testParam2": str}

        assert (test_obj.name) == "dummycommand"
        assert (test_obj.ENDPOINT) == "test"
        assert (test_obj.DATA) == {"testParam2": str}
        assert (test_obj.CMD) == "test_cmd"

    def test_meta_with_name_override(self):
        test_obj = DummyCommand()
        test_obj.name = "testcmd"

        assert (test_obj.name) == "testcmd"
        assert (test_obj.ENDPOINT) == "test"
        assert (test_obj.DATA) == {"testParam": str}
        assert (test_obj.CMD) == "test_cmd"


class RealDummyCommand(TCCommand):
    ENDPOINT = "testCmd"
    CMD = "test"
    DATA = {"testParam": str}

    pass


class SimpleDummyReturn(TCReturnData):
    endpoint: str
    action: str
    result: str
    data: Dict[str, Any]

    def __init__(
        self, endpoint: str, action: str, result: str, data: Dict[str, Any]
    ):
        self.endpoint = endpoint
        self.action = action
        self.result = result
        self.data = data


class BaseCommandAsyncTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(self):
        self._connection = TCConnectionStub()

    async def test_call_noreturn(self):
        test_obj = RealDummyCommand()

        res = await test_obj(connection=self._connection, data=["param"])
        assert res == None

    async def test_call_with_return(self):
        test_obj = RealDummyCommand()
        test_obj.RETURNS = SimpleDummyReturn

        res = await test_obj(connection=self._connection, data=["param"])

        assert type(res) == SimpleDummyReturn
        assert res.endpoint == "testCmd"
        assert res.action == "test"
        assert res.data == {"testParam": "param"}

    async def test_call_invalid_returntype(self):
        test_obj = RealDummyCommand()
        test_obj.RETURNS = str

        with self.assertRaises(TCInvalidReturnType):
            await test_obj(connection=self._connection, data=["param"])

    async def test_call_invalid_return_data(self):
        test_obj = RealDummyCommand()
        test_obj.RETURNS = SimpleDummyReturn
        test_obj.CMD = "otherTest"

        self._connection.bad_response = True

        with self.assertRaises(TCInvalidReturnType):
            await test_obj(connection=self._connection, data=["param"])

        self._connection.bad_response = False

    async def test_call_missing_data(self):
        test_obj = RealDummyCommand()
        test_obj.RETURNS = SimpleDummyReturn
        test_obj.CMD = "otherTest"

        with self.assertRaises(ValueError):
            await test_obj(connection=self._connection, data=[])

    async def test_command_bind(self):
        test_cmd = RealDummyCommand()
        test_cmd.name = "dummy"

        setattr(type(self._connection), test_cmd.name, test_cmd)

        # Check bind on instance
        res = await self._connection.dummy(["param"])
        assert res == None

        # Check bind on class
        res = await type(self._connection).dummy(self._connection, ["param"])
        assert res == None

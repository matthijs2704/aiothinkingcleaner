"""Tests for data structures."""
from typing import Any, Dict

import unittest
from unittest.mock import patch

import pytest

from aiothinkingcleaner.data import TCDeviceState, TCDeviceStatus


def test_stub():
    assert True


def test_devicestatus_init():
    data: Dict[str, Any] = {
        "name": "name",
        "battery_charge": 12.34,
        "capacity": 1234,
        "cleaner_state": TCDeviceState.BASE.value,
        "cleaning": "1",
        "schedule_serial_number": 0,
        "near_homebase": "1",
    }
    dev_stat = TCDeviceStatus(**data)
    assert dev_stat.name == "name"
    assert dev_stat.battery_charge == 12.34
    assert dev_stat.state == TCDeviceState.BASE
    assert dev_stat.is_cleaning
    assert dev_stat.is_near_homebase

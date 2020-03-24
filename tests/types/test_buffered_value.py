# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.types import BufferedValue
from sensirion_shdlc_sensorbridge.i2c_errors import SensorBridgeI2cNackError
import pytest


@pytest.mark.parametrize("rx_data,raw_status,raw_data,error_type", [
    (b"\x00", 0x00, b"", type(None)),
    (b"\x01", 0x01, b"", SensorBridgeI2cNackError),
    (b"\x00\x11\x22\x33", 0x00, b"\x11\x22\x33", type(None)),
    (b"\x01\x11\x22\x33", 0x01, b"\x11\x22\x33", SensorBridgeI2cNackError),
])
def test_members(rx_data, raw_status, raw_data, error_type):
    """
    Test if the BufferedValue members are properly initialized.
    """
    value = BufferedValue(rx_data)
    assert type(value.raw_status) is int
    assert value.raw_status == raw_status
    assert type(value.raw_data) is bytes
    assert value.raw_data == raw_data
    assert type(value.error) == error_type


def test_data_valid():
    """
    Test if the data property returns the correct type and value if no
    error occurred.
    """
    value = BufferedValue(b"\x00\x11\x22\x33")
    assert type(value.data) == bytes
    assert value.data == b"\x11\x22\x33"


def test_data_raises():
    """
    Test if the data property raises the correct exception if an error
    occurred.
    """
    value = BufferedValue(b"\x01\x11\x22\x33")
    with pytest.raises(SensorBridgeI2cNackError):
        value.data

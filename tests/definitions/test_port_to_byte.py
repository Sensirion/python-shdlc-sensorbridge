# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.definitions import SensorBridgePort, \
    port_to_byte
import pytest


@pytest.mark.parametrize("port,accept_all,expected_byte", [
    (SensorBridgePort.ONE, False, 0x00),
    (SensorBridgePort.TWO, False, 0x01),
    (SensorBridgePort.ONE, True, 0x00),
    (SensorBridgePort.TWO, True, 0x01),
    (SensorBridgePort.ALL, True, 0xFF),
])
def test_valid_args(port, accept_all, expected_byte):
    """
    Test if the return value of port_to_byte() is correct when passing
    a valid port.
    """
    byte = port_to_byte(port, accept_all)
    assert type(byte) is int
    assert byte == expected_byte


@pytest.mark.parametrize("port,accept_all", [
    (2, False),
    (2, True),
    (SensorBridgePort.ALL, False),
    ("foo", True),
])
def test_invalid_args(port, accept_all):
    """
    Test if port_to_byte() raises a ValueError when passing an invalid port.
    """
    with pytest.raises(ValueError):
        port_to_byte(port, accept_all)

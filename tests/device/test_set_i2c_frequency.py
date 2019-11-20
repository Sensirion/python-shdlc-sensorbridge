# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,frequency", [
    (SensorBridgePort.ONE, 100000),
    (SensorBridgePort.TWO, 400e3),
    (SensorBridgePort.ALL, 1e6),
])
def test_valid_arguments(device, port, frequency):
    """
    Test if the set_i2c_frequency() function works when passing a valid port
    and a valid frequency.
    """
    result = device.set_i2c_frequency(port, frequency)
    assert result is None


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    "2",
])
def test_invalid_port(device, port):
    """
    Test if the set_i2c_frequency() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.set_i2c_frequency(port, 100e3)


@pytest.mark.needs_device
@pytest.mark.parametrize("frequency", [
    0,
    100,
    100000.1
])
def test_invalid_frequency(device, frequency):
    """
    Test if the set_i2c_frequency() function raises the correct exception when
    passing an invalid frequency.
    """
    with pytest.raises(ValueError):
        device.set_i2c_frequency(SensorBridgePort.ONE, frequency)

# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
from sensirion_shdlc_driver.errors import ShdlcCommandParameterError
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,first_address,last_address", [
    (SensorBridgePort.ONE, 1, 1),
    (SensorBridgePort.TWO, 1, 100),
    (SensorBridgePort.ONE, 100, 100),
    (SensorBridgePort.TWO, 100, 127),
    (SensorBridgePort.ONE, 127, 127),
])
def test_valid_arguments(device, port, first_address, last_address):
    """
    Test if the scan_i2c() function works when passing a valid port
    and valid addresses.
    """
    addresses = device.scan_i2c(port, first_address, last_address)
    assert type(addresses) is list
    for address in addresses:
        assert type(address) is int


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    SensorBridgePort.ALL,
])
def test_invalid_port(device, port):
    """
    Test if the scan_i2c() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.scan_i2c(port, 1, 127)


@pytest.mark.needs_device
@pytest.mark.parametrize("first_address,last_address", [
    (0, 0),
    (0, 100),
    (100, 99),
    (127, 0),
    (127, 128),
    (128, 255),
    (255, 255),
])
def test_invalid_addresses(device, first_address, last_address):
    """
    Test if the scan_i2c() function raises the correct exception when
    passing invalid addresses.
    """
    with pytest.raises(ShdlcCommandParameterError):
        device.scan_i2c(SensorBridgePort.ONE, first_address, last_address)

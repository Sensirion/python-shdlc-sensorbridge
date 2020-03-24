# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,voltage", [
    (SensorBridgePort.ONE, 1.8),
    (SensorBridgePort.TWO, 3),
    (SensorBridgePort.ALL, 1.2),
])
def test_valid_arguments(device, port, voltage):
    """
    Test if the set_supply_voltage() function works when passing valid
    arguments.
    """
    result = device.set_supply_voltage(port, voltage)
    assert result is None


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    "2",
])
def test_invalid_port(device, port):
    """
    Test if the set_supply_voltage() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.set_supply_voltage(port, 1.2)


@pytest.mark.needs_device
@pytest.mark.parametrize("voltage", [
    0,
    1,
    3.1,
])
def test_invalid_voltage(device, voltage):
    """
    Test if the set_supply_voltage() function raises the correct exception when
    passing an invalid voltage.
    """
    with pytest.raises(ValueError):
        device.set_supply_voltage(SensorBridgePort.ONE, voltage)

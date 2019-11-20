# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    SensorBridgePort.ONE,
    SensorBridgePort.TWO,
])
def test_valid_port(device, port):
    """
    Test if the measure_voltage() function works when passing a valid port.
    """
    voltage = device.measure_voltage(port)
    assert type(voltage) is float


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    SensorBridgePort.ALL,
])
def test_invalid_port(device, port):
    """
    Test if the measure_voltage() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.measure_voltage(port)

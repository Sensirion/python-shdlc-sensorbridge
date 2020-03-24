# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    SensorBridgePort.ONE,
    SensorBridgePort.TWO,
    SensorBridgePort.ALL,
])
def test_valid_port(device, port):
    """
    Test if the blink_led() function works when passing a valid port.
    """
    result = device.blink_led(port)
    assert result is None


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    "2",
])
def test_invalid_port(device, port):
    """
    Test if the blink_led() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.blink_led(port)

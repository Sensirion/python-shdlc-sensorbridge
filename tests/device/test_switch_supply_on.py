# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,state", [
    (SensorBridgePort.ONE, True),
    (SensorBridgePort.TWO, False),
    (SensorBridgePort.ALL, False),
])
def test_valid_port(device, port, state):
    """
    Test if the switch_supply_on() function works when passing a valid port.
    """
    result = device.switch_supply_on(port)
    assert result is None


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    "2",
])
def test_invalid_port(device, port):
    """
    Test if the switch_supply_on() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.switch_supply_on(port)

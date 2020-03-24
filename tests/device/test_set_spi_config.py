# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
from sensirion_shdlc_driver.errors import ShdlcCommandParameterError
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,mode,frequency", [
    (SensorBridgePort.ONE, 0, 330000),
    (SensorBridgePort.TWO, 2, 1.0e6),
    (SensorBridgePort.ALL, 3, 21e6),
])
def test_valid_arguments(device, port, mode, frequency):
    """
    Test if the set_spi_config() function works when passing valid arguments.
    """
    result = device.set_spi_config(port, mode, frequency)
    assert result is None


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    "2",
])
def test_invalid_port(device, port):
    """
    Test if the set_spi_config() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.set_spi_config(port, 0, 330e3)


@pytest.mark.needs_device
@pytest.mark.parametrize("mode", [
    4,
    0xFF,
])
def test_invalid_mode(device, mode):
    """
    Test if the set_spi_config() function raises the correct exception when
    passing an invalid mode.
    """
    with pytest.raises(ShdlcCommandParameterError):
        device.set_spi_config(SensorBridgePort.ONE, mode, 330e3)


@pytest.mark.needs_device
@pytest.mark.parametrize("frequency", [
    0,
    100e3,
    600001,
])
def test_invalid_frequency(device, frequency):
    """
    Test if the set_spi_config() function raises the correct exception when
    passing an invalid frequency.
    """
    with pytest.raises(ValueError):
        device.set_spi_config(SensorBridgePort.ONE, 0, frequency)

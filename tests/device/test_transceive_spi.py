# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,tx_data", [
    (SensorBridgePort.ONE, []),  # empty data
    (SensorBridgePort.TWO, [0x00]),  # as list
    (SensorBridgePort.ONE, bytearray([0xFF, 0xFF])),  # as bytearray
    (SensorBridgePort.TWO, b"\x00\x01\x02\xFF"),  # as bytes
])
def test_valid_port(device, port, tx_data):
    """
    Test if the transceive_spi() function works.
    """
    rx_data = device.transceive_spi(port, tx_data)
    assert type(rx_data) is bytes
    assert len(rx_data) == len(tx_data)


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    SensorBridgePort.ALL,
])
def test_invalid_port(device, port):
    """
    Test if the transceive_spi() function raises the correct exception when
    passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.transceive_spi(port, [])

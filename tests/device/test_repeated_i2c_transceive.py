# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort
from sensirion_shdlc_sensorbridge.types import RepeatedTransceiveHandle, \
    ReadBufferResponse
import time
import pytest


@pytest.mark.needs_device
@pytest.mark.parametrize("port,expected_handle_count", [
    (SensorBridgePort.ONE, 1),
    (SensorBridgePort.TWO, 1),
    (SensorBridgePort.ALL, 2),
])
def test_start_read_stop_valid_port(device, port, expected_handle_count):
    """
    Test if the start_repeated_i2c_transceive() and
    stop_repeated_i2c_transceive() functions work when passing a valid port.
    """
    handles = device.start_repeated_i2c_transceive(
        port, interval_us=1e3, address=1, tx_data=[0x00], rx_length=3,
        timeout_us=1e3, read_delay_us=1e3)
    if expected_handle_count == 1:
        handles = (handles,)  # make a tuple
    assert type(handles) is tuple
    assert len(handles) == expected_handle_count
    for handle in handles:
        assert type(handle) is RepeatedTransceiveHandle
        assert 0 <= handle.raw_handle <= 0xFF
        assert handle.rx_length == 3

        time.sleep(0.05)
        buffer = device.read_buffer(handle)
        assert type(buffer) is ReadBufferResponse
        assert len(buffer.values) > 0
        for value in buffer.values:
            assert len(value.raw_data) == 3

        result = device.stop_repeated_i2c_transceive(handle)
        assert result is None


@pytest.mark.needs_device
@pytest.mark.parametrize("port", [
    2,
    "2",
])
def test_invalid_port(device, port):
    """
    Test if the i2c_start_repeated_transceive() function raises the correct
    exception when passing an invalid port.
    """
    with pytest.raises(ValueError):
        device.start_repeated_i2c_transceive(
            port, interval_us=1000, address=1, tx_data=[0x00], rx_length=1,
            timeout_us=1000, read_delay_us=1000)


@pytest.mark.needs_device
def test_stop_all_handles(device):
    """
    Test if the i2c_stop_repeated_transceive() function works when passing
    None (i.e. stop all handles).
    """
    device.start_repeated_i2c_transceive(
        port=1, interval_us=1000, address=1, tx_data=[0x00], rx_length=1,
        timeout_us=1000, read_delay_us=1000)
    result = device.stop_repeated_i2c_transceive(None)
    assert result is None

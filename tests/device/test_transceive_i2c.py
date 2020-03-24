# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.device_errors import SensorBridgeI2cNackError
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice
from mock import MagicMock
import pytest


def test_mocked():
    """
    Test if the transceive_i2c() function sends the correct commands and
    returns the correct data.
    """
    # prepare ShdlcConnection mock and SensorBridgeShdlcDevice object
    connection = MagicMock()
    connection.execute.side_effect = [
        ([0x00, 0x01, 0x02], False),  # first call
        ([0x03, 0x04, 0x05], False),  # second call
        ([0x06, 0x07], False),        # third call
        ([0x08], False),              # fourth call
    ]
    device = SensorBridgeShdlcDevice(connection, 0)

    # execute function under test
    tx_data = 240*[0x11] + 240*[0x22] + 100*[0x33]
    rx_data = device.transceive_i2c(
        port=SensorBridgePort.ONE, address=0x70, tx_data=tx_data,
        rx_length=9, timeout_us=255.0)

    # get all sent command objects (expected four of them)
    sent_commands = [params.args[1]
                     for params in connection.execute.call_args_list]
    assert len(sent_commands) == 4

    # first command contains type,port,address,txlen,rxlen,timeout,txdata
    assert sent_commands[0].data == \
        b"\x00\x00\x70\x00\x00\x02\x44\x00\x00\x00\x09\x00\x00\x00\xFF" \
        + 240*b"\x11"

    # subsequent commands contain type,port,txdata
    assert sent_commands[1].data == b"\x01\x00" + 240*b"\x22"
    assert sent_commands[2].data == b"\x01\x00" + 100*b"\x33"
    assert sent_commands[3].data == b"\x01\x00"

    # response must be equal to all mocked return values appended together
    assert rx_data == [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]


@pytest.mark.needs_device
@pytest.mark.parametrize("port,tx_data,rx_length", [
    (SensorBridgePort.ONE, [], 0),  # no TX, no RX
    (SensorBridgePort.ONE, [0x78, 0x66], 0),  # valid TX, no RX
    (SensorBridgePort.ONE, [0x78, 0x66], 4),  # valid TX, with RX
])
def test_shtc3(device, port, tx_data, rx_length):
    """
    Test if the transceive_i2c() function works when communicating with an
    SHTC3 sensor.
    """
    device.set_i2c_frequency(port, 100e3)
    device.set_supply_voltage(port, 1.8)
    device.switch_supply_on(port)
    rx_data = device.transceive_i2c(
        port, address=0x70, tx_data=tx_data, rx_length=rx_length,
        timeout_us=100000)
    assert type(rx_data) is bytes
    assert len(rx_data) == rx_length


@pytest.mark.needs_device
def test_long_tx(device):
    """
    Test if the transceive_i2c() function raises an I2C NACK error when
    sending a long I2C frame without having a sensor connected.
    """
    with pytest.raises(SensorBridgeI2cNackError):
        device.transceive_i2c(
            port=SensorBridgePort.TWO, address=0x70, tx_data=300*[0x55],
            rx_length=0, timeout_us=100000)


@pytest.mark.needs_device
def test_long_rx(device):
    """
    Test if the transceive_i2c() function works when receiving data longer
    than an SHDLC frame.
    """
    rx_data = device.transceive_i2c(
        port=SensorBridgePort.ONE, address=0x70, tx_data=[0x78, 0x66],
        rx_length=600, timeout_us=1000000)
    assert type(rx_data) is bytes
    assert len(rx_data) == 600

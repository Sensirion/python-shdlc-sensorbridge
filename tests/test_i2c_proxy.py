# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice, SensorBridgeI2cProxy
from sensirion_shdlc_sensorbridge.device_errors import \
    SensorBridgeI2cNackError, SensorBridgeI2cTimeoutError
from mock import MagicMock
import pytest


def test_empty_tx_rx():
    """
    Test if the return value of transceive() is correct if no data is
    transceived.
    """
    device = MagicMock()
    device.transceive_i2c.return_value = b""
    proxy = SensorBridgeI2cProxy(device, SensorBridgePort.TWO)
    status, error, rx_data = proxy.transceive(0x42, None, None, 0.1, 0.2)
    args = [args for args, kwargs in device.transceive_i2c.call_args_list]
    assert args == [(SensorBridgePort.TWO, 0x42, b"", 0, 0.2e6)]
    assert status == SensorBridgeI2cProxy.STATUS_OK
    assert error is None
    assert type(rx_data) is bytes
    assert rx_data == b""


def test_tx_rx():
    """
    Test if the return value of transceive() is correct if there are TX and
    RX data.
    """
    device = MagicMock()
    device.transceive_i2c.return_value = b"\xBE\xEF"
    proxy = SensorBridgeI2cProxy(device, SensorBridgePort.TWO)
    status, error, rx_data = proxy.transceive(0x42, b"\x13", 3, 0.1, 0.2)
    args = [args for args, kwargs in device.transceive_i2c.call_args_list]
    assert args == [(SensorBridgePort.TWO, 0x42, b"\x13", 3, 0.2e6)]
    assert status == SensorBridgeI2cProxy.STATUS_OK
    assert error is None
    assert type(rx_data) is bytes
    assert rx_data == b"\xBE\xEF"


@pytest.mark.parametrize("exception,expected_status", [
    (SensorBridgeI2cNackError, SensorBridgeI2cProxy.STATUS_NACK),
    (SensorBridgeI2cTimeoutError, SensorBridgeI2cProxy.STATUS_TIMEOUT),
])
def test_exceptions(exception, expected_status):
    """
    Test if the return value of transceive() is correct in case of exceptions.
    """
    device = MagicMock()
    device.transceive_i2c.side_effect = exception
    proxy = SensorBridgeI2cProxy(device, SensorBridgePort.ONE)
    status, error, rx_data = proxy.transceive(0x42, b"\x13", 3, 0.1, 0.2)
    assert status == expected_status
    assert type(error) is exception
    assert rx_data == b""


def test_with_mocked_connection():
    """
    Test if the return value of transceive() is correct when using a real
    device object but with a mocked connection.
    """
    # prepare ShdlcConnection mock and SensorBridgeI2cProxy object
    connection = MagicMock()
    connection.execute.return_value = (b"\x11\x22\x33", False)
    device = SensorBridgeShdlcDevice(connection, 0)
    proxy = SensorBridgeI2cProxy(device, SensorBridgePort.ONE)

    # execute function under test
    status, error, rx_data = proxy.transceive(0x70, b"\x13\x37", 3, 255e-6, 0)
    assert status == SensorBridgeI2cProxy.STATUS_OK
    assert error is None
    assert type(rx_data) is bytes
    assert rx_data == b"\x11\x22\x33"

    # check function calls
    sent_commands = [params.args[1]
                     for params in connection.execute.call_args_list]
    assert len(sent_commands) == 1

    # command contains type,port,address,txlen,rxlen,timeout,txdata
    assert sent_commands[0].data == \
        b"\x00\x00\x70\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\xFF\x13\x37"


@pytest.mark.needs_device
def test_shtc3(device):
    """
    Test if the return value of transceive() is correct when using a real
    device.
    """
    device.set_i2c_frequency(SensorBridgePort.ONE, 100e3)
    device.set_supply_voltage(SensorBridgePort.ONE, 1.8)
    device.switch_supply_on(SensorBridgePort.ONE)
    proxy = SensorBridgeI2cProxy(device, SensorBridgePort.ONE)
    status, error, rx_data = proxy.transceive(0x70, b"\x78\x66", 4, 0.1, 0)
    assert status == SensorBridgeI2cProxy.STATUS_OK
    assert error is None
    assert type(rx_data) is bytes
    assert len(rx_data) == 4

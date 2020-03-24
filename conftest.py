# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice
import platform
import pytest


# Choose a reasonable default serial port where the SensorBridge could be
# connected, depending on the operating system.
if platform.system().lower() == 'windows':
    DEFAULT_PORT = 'COM2'  # COM1 is usually the built-in port, so skip it
else:
    DEFAULT_PORT = '/dev/ttyUSB0'  # First virtual serial port


def pytest_addoption(parser):
    """
    Register command line options
    """
    parser.addoption("--serial-port", action="store", default=DEFAULT_PORT)


def pytest_report_header(config):
    """
    Add extra information to test report header
    """
    return "serial port: " + config.getoption("--serial-port")


@pytest.fixture(scope="session")
def connection(request):
    serial_port = request.config.getoption("--serial-port")
    with ShdlcSerialPort(serial_port, 460800) as port:
        connection = ShdlcConnection(port)
        yield connection


@pytest.fixture
def device(connection):
    device = SensorBridgeShdlcDevice(connection, 0)

    # check firmware version of the DUT (some tests would fail with a too
    # old firmware)
    fw_version = device.get_version().firmware
    assert (fw_version.major == 5) and (fw_version.minor >= 8)

    # reset state of device to a safe state to avoid sensor damage caused by
    # too high voltage or so
    device.switch_supply_off(SensorBridgePort.ALL)
    device.set_supply_voltage(SensorBridgePort.ALL, 1.2)

    yield device

    # make sure the ports are powered off after executing tests
    device.switch_supply_off(SensorBridgePort.ALL)

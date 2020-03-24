# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcSerialPort, ShdlcConnection
from sensirion_shdlc_sensorbridge import SensorBridgePort, \
    SensorBridgeShdlcDevice
import pytest


def pytest_addoption(parser):
    """
    Register command line options
    """
    parser.addoption("--serial-port", action="store", type=str)


def _get_serial_port(config, validate=False):
    """
    Get the serial port to be used for the tests.
    """
    port = config.getoption("--serial-port")
    if (validate is True) and (port is None):
        raise ValueError("Please specify the serial port to be used with "
                         "the '--serial-port' argument.")
    return port


def pytest_report_header(config):
    """
    Add extra information to test report header
    """
    return "serial port: " + str(_get_serial_port(config))


@pytest.fixture(scope="session")
def serial_port(request):
    """
    Fixture to get the serial port to be used for the tests.
    """
    return _get_serial_port(request.config, validate=True)


@pytest.fixture(scope="session")
def connection(serial_port):
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

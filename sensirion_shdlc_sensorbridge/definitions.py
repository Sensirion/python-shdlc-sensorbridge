# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from enum import IntEnum

import logging
log = logging.getLogger(__name__)


class SensorBridgePort(IntEnum):
    """
    An enum containing all available ports with their corresponding byte
    values how they are transmitted over SHDLC.
    """
    ONE = 0x00  #: Port 1
    TWO = 0x01  #: Port 2
    ALL = 0xFF  #: All ports


#: A dictionary containing all available voltages with their corresponding
#: byte values how they are transmitted over SHDLC.
VOLTAGES = {
    1.2: 0x00,  # 1.2V
    1.5: 0x04,  # 1.5V
    1.8: 0x01,  # 1.8V
    2.1: 0x05,  # 2.1V
    2.4: 0x06,  # 2.4V
    2.7: 0x07,  # 2.7V
    3.0: 0x08,  # 3.0V
    3.3: 0x02,  # 3.3V
    3.6: 0x09,  # 3.6V
    4.5: 0x0A,  # 4.5V
    5.0: 0x03,  # 5.0V
    5.5: 0x0B,  # 5.5V
}

#: A dictionary containing all available I2C frequencies with their
#: corresponding byte values how they are transmitted over SHDLC.
I2C_FREQUENCIES = {
    10e3: 0x04,  # 10kHz
    50e3: 0x05,  # 50kHz
    100e3: 0x00,  # 100kHz
    400e3: 0x01,  # 400kHz
    1e6: 0x02,  # 1MHz
    2e6: 0x03,  # 2MHz
}

#: A dictionary containing all available SPI frequencies with their
#: corresponding byte values how they are transmitted over SHDLC.
SPI_FREQUENCIES = {
    330e3: 0x00,  # 330kHz
    600e3: 0x01,  # 600kHz
    1e6: 0x02,  # 1MHz
    5e6: 0x03,  # 5MHz
    10e6: 0x04,  # 10MHz
    21e6: 0x05,  # 21MHz
}


def port_to_byte(port, accept_all):
    """
    Convert a port value to the corresponding byte value.

    :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
        The port to convert.
    :param accept_all:
        If True, the value
        :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
        is accepted.
    :raises ValueError:
        If the passed port is not valid.
    :return:
        The corresponding byte value of the port.
    :rtype: byte
    """
    accepted_values = list(SensorBridgePort)
    if not accept_all:
        accepted_values.remove(SensorBridgePort.ALL)
    if port in accepted_values:
        return int(port)
    else:
        raise ValueError("Invalid port '{}' specified. Supported values are "
                         "{}.".format(port, accepted_values))


def voltage_to_byte(voltage):
    """
    Convert a voltage in Volts to the corresponding byte value.

    :param int/float port:
        The voltage to convert.
    :raises ValueError:
        If the passed voltage is not supported.
    :return:
        The corresponding byte value of the voltage.
    :rtype: byte
    """
    if voltage in VOLTAGES:
        return VOLTAGES[voltage]
    else:
        raise ValueError("Invalid voltage '{}' specified. Supported values "
                         "are {}.".format(voltage, list(VOLTAGES.keys())))


def i2c_frequency_to_byte(frequency):
    """
    Convert an I2C frequency in Hz to the corresponding byte value.

    :param int/float port:
        The frequency to convert.
    :raises ValueError:
        If the passed frequency is not supported.
    :return:
        The corresponding byte value of the frequency.
    :rtype: byte
    """
    if frequency in I2C_FREQUENCIES:
        return I2C_FREQUENCIES[frequency]
    else:
        raise ValueError("Invalid I2C frequency '{}' specified. Supported "
                         "values are {}.".format(frequency,
                                                 list(I2C_FREQUENCIES.keys())))


def spi_frequency_to_byte(frequency):
    """
    Convert an SPI frequency in Hz to the corresponding byte value.

    :param int/float port:
        The frequency to convert.
    :raises ValueError:
        If the passed frequency is not supported.
    :return:
        The corresponding byte value of the frequency.
    :rtype: byte
    """
    if frequency in SPI_FREQUENCIES:
        return SPI_FREQUENCIES[frequency]
    else:
        raise ValueError("Invalid SPI frequency '{}' specified. Supported "
                         "values are {}.".format(frequency,
                                                 list(SPI_FREQUENCIES.keys())))

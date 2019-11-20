# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.definitions import voltage_to_byte
import pytest


@pytest.mark.parametrize("voltage,expected_byte", [
    (1.2, 0x00),
    (1.80, 0x01),
    (3.3, 0x02),
    (5, 0x03),
    (1.5e0, 0x04),
    (2.1, 0x05),
    (2.4, 0x06),
    (2.7, 0x07),
    (3e0, 0x08),
    (3.6, 0x09),
    (4.5, 0x0A),
    (5.5, 0x0B),
])
def test_valid_args(voltage, expected_byte):
    """
    Test if the return value of voltage_to_byte() is correct when passing
    a valid voltage.
    """
    byte = voltage_to_byte(voltage)
    assert type(byte) is int
    assert byte == expected_byte


@pytest.mark.parametrize("voltage", [
    0,
    0.0,
    1,
    1.0,
    '3.3',
    10e0,
])
def test_invalid_args(voltage):
    """
    Test if voltage_to_byte() raises a ValueError when passing an invalid
    voltage.
    """
    with pytest.raises(ValueError):
        voltage_to_byte(voltage)

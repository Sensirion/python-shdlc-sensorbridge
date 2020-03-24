# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.definitions import i2c_frequency_to_byte
import pytest


@pytest.mark.parametrize("frequency,expected_byte", [
    (100000, 0x00),
    (400e3, 0x01),
    (1.0e6, 0x02),
    (2000000, 0x03),
    (0.01e6, 0x04),
    (50000.0, 0x05),
])
def test_valid_args(frequency, expected_byte):
    """
    Test if the return value of i2c_frequency_to_byte() is correct when
    passing a valid frequency.
    """
    byte = i2c_frequency_to_byte(frequency)
    assert type(byte) is int
    assert byte == expected_byte


@pytest.mark.parametrize("frequency", [
    0,
    0.0,
    1,
    1.0,
    '10000',
    10e0,
    10000.01,
    10001,
])
def test_invalid_args(frequency):
    """
    Test if i2c_frequency_to_byte() raises a ValueError when passing an
    invalid frequency.
    """
    with pytest.raises(ValueError):
        i2c_frequency_to_byte(frequency)

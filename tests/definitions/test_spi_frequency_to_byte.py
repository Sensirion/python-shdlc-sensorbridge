# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.definitions import spi_frequency_to_byte
import pytest


@pytest.mark.parametrize("frequency,expected_byte", [
    (330000, 0x00),
    (600e3, 0x01),
    (1.0e6, 0x02),
    (5000000, 0x03),
    (10000e3, 0x04),
    (21000000.0, 0x05),
])
def test_valid_args(frequency, expected_byte):
    """
    Test if the return value of spi_frequency_to_byte() is correct when
    passing a valid frequency.
    """
    byte = spi_frequency_to_byte(frequency)
    assert type(byte) is int
    assert byte == expected_byte


@pytest.mark.parametrize("frequency", [
    0,
    0.0,
    1,
    1.0,
    '1000000',
    10e0,
    1000000.1,
    1000001,
])
def test_invalid_args(frequency):
    """
    Test if spi_frequency_to_byte() raises a ValueError when passing an
    invalid frequency.
    """
    with pytest.raises(ValueError):
        spi_frequency_to_byte(frequency)

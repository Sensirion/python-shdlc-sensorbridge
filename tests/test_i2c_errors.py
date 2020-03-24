# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.i2c_errors import i2c_error_from_code, \
    SensorBridgeI2cError, SensorBridgeI2cNackError, \
    SensorBridgeI2cTimeoutError, SensorBridgeI2cTimingError
import pytest


@pytest.mark.parametrize("code,expected_return_type", [
    (0x00, None),
    (0x01, SensorBridgeI2cNackError),
    (0x02, SensorBridgeI2cTimeoutError),
    (0x03, SensorBridgeI2cTimingError),
    (0x04, SensorBridgeI2cError),
])
def test(code, expected_return_type):
    """
    Test if the return values of i2c_error_from_code() are correct.
    """
    error = i2c_error_from_code(code)
    if expected_return_type is None:
        assert error is None
    else:
        assert type(error) == expected_return_type
        assert error.error_code == code
        assert len(error.error_message) > 0

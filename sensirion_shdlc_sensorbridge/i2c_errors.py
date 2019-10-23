# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

import logging
log = logging.getLogger(__name__)


class SensorBridgeI2cError(IOError):
    """
    I2C transceive error.
    """
    def __init__(self, code, message="Unknown"):
        super(SensorBridgeI2cError, self).__init__(
            "I2C transceive error: {}".format(message)
        )
        self.error_code = code
        self.error_message = message


class SensorBridgeI2cNackError(SensorBridgeI2cError):
    """
    I2C transceive NACK error.
    """
    def __init__(self):
        super(SensorBridgeI2cNackError, self).__init__(
            0x01,
            "NACK (byte not acknowledged)"
        )


class SensorBridgeI2cTimeoutError(SensorBridgeI2cError):
    """
    I2C transceive timeout error.
    """
    def __init__(self):
        super(SensorBridgeI2cTimeoutError, self).__init__(
            0x02,
            "Timeout"
        )


class SensorBridgeI2cTimingError(SensorBridgeI2cError):
    """
    I2C repeated transceive timing error.
    """
    def __init__(self):
        super(SensorBridgeI2cTimingError, self).__init__(
            0x03,
            "Invalid timing (frequency, interval, timeout or delay)"
        )


"""
List containing all I2C errors specified in this file.
"""
SENSORBRIDGE_I2C_ERROR_LIST = [
    SensorBridgeI2cNackError(),
    SensorBridgeI2cTimeoutError(),
    SensorBridgeI2cTimingError(),
]


def i2c_error_from_code(code):
    """
    Return the corresponding exception for a given I2C error code.

    :param byte code:
        Error code as received from the device.
    :return:
        The exception for the given error code. If code is zero (no error),
        None is returned.
    :rtype:
        None or an instance of
        :py:class:`~sensirion_shdlc_sensorbridge.i2c_errors.SensorBridgeI2cError`
    """  # noqa: E501
    if code == 0:
        return None
    for error in SENSORBRIDGE_I2C_ERROR_LIST:
        if error.error_code == code:
            return error
    return SensorBridgeI2cError(code)  # fallback for unknown error codes

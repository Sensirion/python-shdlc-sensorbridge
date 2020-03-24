# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from .device_errors import SensorBridgeI2cNackError, \
    SensorBridgeI2cTimeoutError

import logging
log = logging.getLogger(__name__)


class SensorBridgeI2cProxy(object):
    """
    I²C proxy class to access one of the SEK-SensorBridge ports using the
    unified API defined in the ``sensirion-i2c-driver`` package. Note that this
    package is not publicly available yet, it will be published soon.
    """
    API_VERSION = 1  #: API version (accessed by I2cConnection)

    # Status codes
    STATUS_OK = 0  #: Status code for "transceive operation succeeded".
    STATUS_CHANNEL_DISABLED = 1  #: Status code for "channel disabled error".
    STATUS_NACK = 2  #: Status code for "not acknowledged error".
    STATUS_TIMEOUT = 3  #: Status code for "timeout error".
    STATUS_UNSPECIFIED_ERROR = 4  #: Status code for "unspecified error".

    def __init__(self, device, port):
        """
        Create an I²C proxy for a certain SensorBridge port.

        :param ~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice device:
            The SensorBridge device to communicate with.
        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port to be used for the I²C transceive operation. Note that
            :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
            is not supported here.
        """  # noqa: E501
        super(SensorBridgeI2cProxy, self).__init__()
        self._device = device
        self._port = port

    @property
    def description(self):
        """
        Description of the transceiver.

        For details (e.g. return value documentation), please refer to
        :py:attr:`~sensirion_i2c_driver.transceiver_v1.I2cTransceiverV1.description`.
        """
        return "SensorBridge"

    @property
    def channel_count(self):
        """
        Channel count of this transceiver.

        For details (e.g. return value documentation), please refer to
        :py:attr:`~sensirion_i2c_driver.transceiver_v1.I2cTransceiverV1.channel_count`.
        """
        return None  # single channel transceiver

    def transceive(self, slave_address, tx_data, rx_length, read_delay,
                   timeout):
        """
        Transceive an I²C frame.

        For details (e.g. parameter documentation), please refer to
        :py:meth:`~sensirion_i2c_driver.transceiver_v1.I2cTransceiverV1.transceive`.
        """
        assert type(slave_address) is int
        assert (tx_data is None) or (type(tx_data) is bytes)
        assert (rx_length is None) or (type(rx_length) is int)
        assert type(read_delay) in [float, int]
        assert type(timeout) in [float, int]

        # SensorBridge does not support a read delay, but it automatically
        # retries reading data until the timeout is elapsed. Thus we can just
        # use the read delay as timeout (resp. whichever is greater).
        total_timeout_us = max(read_delay, timeout) * 1e6
        try:
            rx_data = self._device.transceive_i2c(
                self._port, slave_address, tx_data or b"", rx_length or 0,
                total_timeout_us)
            return self.STATUS_OK, None, rx_data
        except SensorBridgeI2cNackError as e:
            return self.STATUS_NACK, e, b""
        except SensorBridgeI2cTimeoutError as e:
            return self.STATUS_TIMEOUT, e, b""

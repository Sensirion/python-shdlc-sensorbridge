# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver.errors import ShdlcResponseError
from .i2c_errors import i2c_error_from_code

import logging
log = logging.getLogger(__name__)


class RepeatedTransceiveHandle(object):
    """
    Represents a handle to a repeated I2C transceive operation. Use only
    internally, usually users don't have to care about this type.
    """
    def __init__(self, raw_handle, rx_length):
        """
        Creates a new handle.

        :param byte raw_handle:
            Handle as returned from the "start repeated transceive" command.
        :param rx_length:
            Number of bytes which the corresponding repeated transceive
            reads from the I2C device.
        """
        super(RepeatedTransceiveHandle, self).__init__()

        #: The raw handle (byte) as received from SensorBridge.
        self.raw_handle = raw_handle

        #: The response length (int) of the corresponding repeated transceive
        #: operation.
        self.rx_length = rx_length


class BufferedValue(object):
    """
    Represents a buffered value from a repeated I2C transceive operation. It
    interprets the raw status and RX data from the buffer and provides a
    convenient API to access them.

    With the :py:attr:`raw_status` and :py:attr:`raw_data` you can access the
    raw data as received from the device. But the property
    :py:meth:`~sensirion_shdlc_sensorbridge.types.BufferedValue.data` provides
    a more convenient interface since it returns the data if it is valid and
    raises an exception if it is not valid.

    :param bytes rx_data:
        The raw buffer data as received from the device.
    """
    def __init__(self, rx_data):
        """
        Creates an instance from the received raw data.

        :param str rx_data:
            Received raw data from SensorBridge, containing the status byte
            and the received data from the I2C read operation.
        """
        super(BufferedValue, self).__init__()

        #: The raw status (byte) of the I2C transceive operation.
        self.raw_status = bytearray(rx_data)[0]

        #: The raw received I2C data. Attention: This data might be invalid if
        #: the transceive operation was not successful!
        self.raw_data = rx_data[1:]

        #: An exception of the occurred I2C error or None if the transceive
        #: operation was successful.
        self.error = i2c_error_from_code(self.raw_status)

    @property
    def data(self):
        """
        Returns the received data if it is valid, or raises an exception if
        an I2C error occurred.

        :raises ~sensirion_shdlc_sensorbridge.i2c_errors.SensorBridgeI2cError:
            If an I2C error occurred, i.e. no valid data is available.
        :return:
            The received bytes.
        :rtype:
            bytes
        """
        if self.error is None:
            return self.raw_data
        else:
            raise self.error


class ReadBufferResponse(object):
    """
    Helper class representing the response to the "read buffer" command,
    i.e. of the method
    :py:meth:`~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice.read_buffer`.

    The class provides some public members which you can access directly.
    """  # noqa: E501
    def __init__(self, rx_length, lost_bytes, remaining_bytes, rx_data):
        """
        Creates an instance from the raw data received from the device.

        :param int rx_length:
            The read data length of the repeated transceive from which the
            response is coming from.
        :param int lost_bytes:
            Number of bytes lost (received from the "read buffer" command).
        :param int remaining_bytes:
            Number of bytes remaining in the buffer (received from the
            "read buffer" command).
        :param bytes rx_data:
            Raw received data bytes containing multiple I2C response status and
            data received from the I2C device.
        """
        super(ReadBufferResponse, self).__init__()

        #: Number of lost bytes (int) due to buffer overrun.
        self.lost_bytes = lost_bytes

        #: Number of remaining bytes in the buffer after reading it. If the
        #: whole buffer was read out, this is zero.
        self.remaining_bytes = remaining_bytes

        #: The received values (list of
        #: :py:class:`~sensirion_shdlc_sensorbridge.types.BufferedValue`)
        self.values = []

        # Check if the received data is a multiple of the expected packet size
        packet_length = rx_length + 1  # rx_length plus status byte
        if (len(rx_data) % packet_length) != 0:
            raise ShdlcResponseError(
                "Received data length ({}) is not a multiple of the expected "
                "packet length ({}).".format(len(rx_data), packet_length),
                rx_data)

        # Split raw rx_data into packets and interpret them
        number_of_packets = len(rx_data) // packet_length
        for i in range(0, number_of_packets):
            start_index = i * packet_length
            packet_data = rx_data[start_index:start_index + packet_length]
            self.values.append(BufferedValue(packet_data))

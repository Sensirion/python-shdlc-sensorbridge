# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver import ShdlcDevice, ShdlcFirmwareUpdate
from .device_errors import SENSORBRIDGE_DEVICE_ERROR_LIST
from .firmware_image import SensorBridgeFirmwareImage
from .definitions import port_to_byte, voltage_to_byte, \
    i2c_frequency_to_byte, spi_frequency_to_byte
from .types import RepeatedTransceiveHandle, ReadBufferResponse
from .commands import \
    SensorBridgeCmdSetPortVoltage, \
    SensorBridgeCmdPortVoltageOnOff, \
    SensorBridgeCmdSetI2cFrequency, \
    SensorBridgeCmdI2cScan, \
    SensorBridgeCmdFirstTransceive, \
    SensorBridgeCmdSubsequentTransceive, \
    SensorBridgeCmdI2cRepeatedTransceive, \
    SensorBridgeCmdReadBuffer, \
    SensorBridgeCmdStopRepeatedTransceive, \
    SensorBridgeCmdSpiConfig, \
    SensorBridgeCmdSpiTransceive, \
    SensorBridgeCmdBlink, \
    SensorBridgeCmdAnalogMeasurement

import logging
log = logging.getLogger(__name__)


class SensorBridgeShdlcDevice(ShdlcDevice):
    """
    SEK-SensorBridge device.

    This is a low-level driver which just provides all SHDLC commands as Python
    methods. Typically, calling a method sends one SHDLC request to the device
    and interprets its response. There is no higher level functionality
    available, please look for other drivers if you need a higher level
    interface.

    There is no (or very few) caching functionality in this driver. For example
    if you call :func:`get_serial_number` 100 times, it will send the command
    100 times over the SHDLC interface to the device. This makes the driver
    (nearly) stateless.
    """

    def __init__(self, connection, slave_address):
        """
        Create a SensorBridge device instance on an SHDLC connection.

        .. note:: This constructor does not communicate with the device, so
                  it's possible to instantiate an object even if the device is
                  not connected or powered yet.

        :param ~sensirion_shdlc_driver.connection.ShdlcConnection connection:
            The connection used for the communication.
        :param byte slave_address:
            The address of the device. The default address of the
            SEK-SensorBridge is 0.
        """
        super(SensorBridgeShdlcDevice, self).__init__(
            connection, slave_address
        )
        self._register_device_errors(SENSORBRIDGE_DEVICE_ERROR_LIST)

    def blink_led(self, port):
        """
        Let the LEDs on the device blink. Useful for example to identify the
        device on a bus.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) which should blink.
        """
        raw_port = port_to_byte(port, accept_all=True)
        self.execute(SensorBridgeCmdBlink(raw_port))

    def measure_voltage(self, port):
        """
        Triggers an analog measurement at the AIN pin. The measured voltage
        is always positive and in the range of 0-5.5V.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port where the measurement should be executed. Note that
            :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
            is not supported here.
        :return: Measured voltage in Volts.
        :rtype: float
        """
        raw_port = port_to_byte(port, accept_all=False)
        return self.execute(SensorBridgeCmdAnalogMeasurement(raw_port))

    def set_supply_voltage(self, port, voltage):
        """
        Sets the supply voltage of a port to a certain value.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) where the voltage should be set.
        :param int/float voltage:
            The voltage to set in Volts. See
            :py:obj:`~sensirion_shdlc_sensorbridge.definitions.VOLTAGES`
            for the list of supported values.
        """
        raw_port = port_to_byte(port, accept_all=True)
        raw_voltage = voltage_to_byte(voltage)
        self.execute(SensorBridgeCmdSetPortVoltage(raw_port, raw_voltage))

    def switch_supply_on(self, port):
        """
        Switches a port supply on. The previously set voltage will be applied.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) to switch on.
        """
        raw_port = port_to_byte(port, accept_all=True)
        self.execute(SensorBridgeCmdPortVoltageOnOff(raw_port, 1))

    def switch_supply_off(self, port):
        """
        Switches a port supply off.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) to switch off.
        """
        raw_port = port_to_byte(port, accept_all=True)
        self.execute(SensorBridgeCmdPortVoltageOnOff(raw_port, 0))

    def set_i2c_frequency(self, port, frequency):
        """
        Sets the I2C frequency to the desired value. The default frequency is
        400kHz.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) where the frequency should be set.
        :param int/float frequency:
            The frequency to set in Hz (e.g. 400'000 for 400kHz). See
            :py:obj:`~sensirion_shdlc_sensorbridge.definitions.I2C_FREQUENCIES`
            for the list of supported values.
        """
        raw_port = port_to_byte(port, accept_all=True)
        raw_frequency = i2c_frequency_to_byte(frequency)
        self.execute(SensorBridgeCmdSetI2cFrequency(raw_port, raw_frequency))

    def scan_i2c(self, port, first_address=1, last_address=127):
        """
        Scans for I2C devices on a specific port within a certain address
        range.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port where the scan should be executed. Note that
            :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
            is not supported here.
        :param byte first_address:
            First address to scan (1..127), defaults to 1.
        :param byte last_address:
            Last address to scan (1..127 and >= first address),
            defaults to 127.
        :return: List of addresses which responded to the scan. Empty list if
            no device responded.
        :rtype: list of byte
        """
        raw_port = port_to_byte(port, accept_all=False)
        response = self.execute(SensorBridgeCmdI2cScan(raw_port, first_address,
                                                       last_address))
        return list(bytearray(response))  # Py2/3 compatible conversion to list

    def transceive_i2c(self, port, address, tx_data, rx_length, timeout_us):
        """
        Transceives an I2C frame on a certain port.

        .. note:: If an I2C error (NACK or timeout) occured, this method raises
                  an exception. So the returned RX data is guaranteed to be
                  valid in terms of there was no I2C communication issue.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port where the transceive should be executed. Note that
            :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
            is not supported here.
        :param byte address:
            I2C address of the targeted device.
        :param bytes-like/list tx_data:
            Raw data (bytes) to send. Pass an empty list or bytes-like object
            if no write operation is needed.
        :param int rx_length:
            Number of bytes to receive.
        :param int/float timeout_us:
            I2C timeout (in Microseconds) when reading bytes. If a frame is
            NACK'd it will be retried up to the timeout value. Same applies
            for clock stretching. Note that floats can be passes for
            convenience, they will be casted to integer internally.
        :return: Received data from the I2C read operation. Empty bytes if
            no data was read.
        :rtype: bytes
        """
        raw_port = port_to_byte(port, accept_all=False)
        max_tx_len_per_frame = 255 - 15  # max frame length minus fixed payload

        log.debug("SensorBridgeShdlcDevice transceive I2C frame with "
                  "address=0x{:2X} rx_length={} timeout={}us tx_data=[{}]"
                  .format(address, rx_length, int(timeout_us), ", ".join(
                      ["0x%.2X" % i for i in bytearray(tx_data)])))

        # first frame
        tx_len_sent = min(len(tx_data), max_tx_len_per_frame)
        rx_data = self.execute(SensorBridgeCmdFirstTransceive(
            raw_port, address, len(tx_data), rx_length, int(timeout_us),
            tx_data[0:tx_len_sent]))

        # send remaining TX data
        while tx_len_sent < len(tx_data):
            tx_len = min(len(tx_data) - tx_len_sent, max_tx_len_per_frame)
            rx_data += self.execute(SensorBridgeCmdSubsequentTransceive(
                raw_port, tx_data[tx_len_sent:tx_len_sent + tx_len]))
            tx_len_sent += tx_len

        # receive remaining RX data
        while len(rx_data) < rx_length:
            rx = self.execute(SensorBridgeCmdSubsequentTransceive(
                raw_port, []))
            assert len(rx) > 0
            rx_data += rx

        log.debug("SensorBridgeShdlcDevice received I2C frame: [{}]".format(
                  ", ".join(["0x%.2X" % i for i in bytearray(rx_data)])))

        return rx_data

    def start_repeated_i2c_transceive(self, port, interval_us, address,
                                      tx_data, rx_length, timeout_us,
                                      read_delay_us=0):
        """
        Starts an asynchronous I2C transceive command in a specific interval.
        Multiple parallel repeated transceives are possible. The returned
        data is stored in a buffer and can be read out with the
        :py:meth:`~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice.read_buffer`
        method.

        .. note:: This method returns a handle for each repeated transceive
                  operation. You have to store these handles since they are
                  needed to fetch the received data with
                  :py:meth:`~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice.read_buffer`
                  and to stop the transceive with
                  :py:meth:`~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice.stop_repeated_i2c_transceive`.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) where the repeated transceive should be started.
        :param int/float interval_us:
            The interval in Microseconds. Note that floats can be passes for
            convenience, they will be casted to integer internally.
        :param byte address:
            I2C address of the targeted device.
        :param bytes-like/list tx_data:
            Raw data (bytes) to send. Pass an empty list or bytes-like object
            if no write operation is needed.
        :param int rx_length:
            Number of bytes to receive. Set to zero if no read operation is
            needed.
        :param int/float timeout_us:
            I2C timeout (in Microseconds) when reading bytes. If a frame is
            NACK'd it will be retried up to the timeout value. Same applies
            for clock stretching. Note that floats can be passes for
            convenience, they will be casted to integer internally.
        :param int/float read_delay_us:
            This time (in Microseconds) will be inserted between the write and
            the read frame to allow a device taking a certain amount of time
            for its measurements. The delay must be smaller than the specified
            timeout. Defaults to 0, i.e. no delay is inserted. Note that
            floats can be passes for convenience, they will be casted to
            integer internally.
        :return:
            Either one handle or two handles for the started transceive
            operations, depending on whether the transceive was started on
            a single channel or on both channels. If
            :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
            was passed as port, a tuple of two handles is returned.
        :rtype:
            :py:class:`~sensirion_shdlc_sensorbridge.types.RepeatedTransceiveHandle`
            or a tuple of it
        """
        raw_port = port_to_byte(port, accept_all=True)
        raw_handles = self.execute(SensorBridgeCmdI2cRepeatedTransceive(
            int(interval_us), raw_port, address, len(tx_data), rx_length,
            int(timeout_us), int(read_delay_us), tx_data))
        handles = [RepeatedTransceiveHandle(h, rx_length)
                   for h in bytearray(raw_handles)]
        return handles[0] if len(handles) == 1 else tuple(handles)

    def stop_repeated_i2c_transceive(self, handle=None):
        """
        Stops a repeated transceive operation.

        :param ~sensirion_shdlc_sensorbridge.types.RepeatedTransceiveHandle handle:
            The handle of the repeated transceive which should be stopped
            (the object which was returned by
            :py:meth:`~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice.start_repeated_i2c_transceive`
            ). Pass None (the default) to stop all active repeated transceives.
        """  # noqa: E501
        raw_handle = 0xFF if (handle is None) else handle.raw_handle
        self.execute(SensorBridgeCmdStopRepeatedTransceive(raw_handle))

    def read_buffer(self, handle, max_reads=100):
        """
        Reads data stored in the buffer of a repeated transceive.

        This method sends "read buffer" commands to the device until the whole
        buffer was read out (since the SHDLC frame length is limited, it's not
        possible to read out the whole buffer with a single command). The
        received values will automatically be removed from the buffer in the
        device, so you will only get the values received since the last call
        to this method.

        .. warning:: If you call this method too rarely, the buffer in the
                     device will overrun, i.e. the oldest values are lost. You
                     should check for lost values by reading the property
                     :py:attr:`~sensirion_shdlc_sensorbridge.types.ReadBufferResponse.lost_bytes`
                     of the returned object. This method does not raise an
                     exception if there are values lost since depending on the
                     use-case, this might be expected behavior.

        .. note:: If the buffer gets filled faster than you read it out, it's
                  not possible to read out the whole buffer. In that case, the
                  property
                  :py:attr:`~sensirion_shdlc_sensorbridge.types.ReadBufferResponse.remaining_bytes`
                  of the returned object will hold a value greater than zero.
                  You might want to check this property to be sure the whole
                  buffer was read out. However, often that's not needed since
                  sooner or later you will also get a buffer overrun in this
                  situation.

        .. note:: This method doesn't raise an exception if there occurred
                  I2C errors (e.g. NACK or timeout) in the transceived I2C
                  frames because this might be expected behavior in some cases.
                  In addition, if only some of the frames contain errors,
                  probably you still want to get all the valid frames. See
                  documentation of
                  :py:class:`~sensirion_shdlc_sensorbridge.types.BufferedValue`
                  to see how to get exceptions in case of I2C errors.

        :param ~sensirion_shdlc_sensorbridge.types.RepeatedTransceiveHandle handle:
            The handle of the repeated transceive from which the data should be
            returned (the object which was returned by
            :py:meth:`~sensirion_shdlc_sensorbridge.device.SensorBridgeShdlcDevice.start_repeated_i2c_transceive`).
        :param int max_reads:
            The maximum count of read commands which should be sent until the
            read operation will be aborted. This abort condition is needed to
            avoid an infinite loop if the buffer gets filled faster than it
            can be read out.
        :return:
            A buffer object containing some metadata and the buffered data
            received from the I2C device. See
            :py:class:`~sensirion_shdlc_sensorbridge.types.ReadBufferResponse`
            for details.
        :rtype:
            :py:class:`~sensirion_shdlc_sensorbridge.types.ReadBufferResponse`
        """  # noqa: E501
        total_lost_bytes = 0
        total_rx_data = bytes()
        for i in range(0, max_reads):
            lost_bytes, remaining_bytes, rx_data = \
                self.execute(SensorBridgeCmdReadBuffer(handle.raw_handle))
            total_lost_bytes += lost_bytes
            total_rx_data += rx_data
            if remaining_bytes == 0:
                break
        return ReadBufferResponse(handle.rx_length, total_lost_bytes,
                                  remaining_bytes, total_rx_data)

    def set_spi_config(self, port, mode, frequency):
        """
        Sets the SPI mode and frequency.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port(s) which should be configured.
        :param byte mode:
            The SPI mode to use. Allowed values are [0, 1, 2, 3].
        :param int/float frequency:
            The frequency to set in Hz (e.g. 330'000 for 330kHz). See
            :py:obj:`~sensirion_shdlc_sensorbridge.definitions.SPI_FREQUENCIES`
            for the list of supported values.
        """
        raw_port = port_to_byte(port, accept_all=True)
        raw_mode = int(mode)
        raw_frequency = spi_frequency_to_byte(frequency)
        self.execute(SensorBridgeCmdSpiConfig(raw_port, raw_mode,
                                              raw_frequency))

    def transceive_spi(self, port, tx_data):
        """
        Transceives an SPI frame on a certain port.

        :param ~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort port:
            The port where the transceive should be executed. Note that
            :py:attr:`~sensirion_shdlc_sensorbridge.definitions.SensorBridgePort.ALL`
            is not supported here.
        :param bytes-like/list tx_data:
            Raw data (bytes) to send.
        :return:
            Received bytes (same number of bytes as tx_data).
        :rtype: bytes
        """
        raw_port = port_to_byte(port, accept_all=False)
        return self.execute(SensorBridgeCmdSpiTransceive(
            raw_port, len(tx_data), tx_data))

    def update_firmware(self, image, emergency=False, status_callback=None,
                        progress_callback=None):
        """Update the firmware on the device.

        This method allows you to download a new firmware (provided as a
        \\*.hex file) to the device. A device reset is performed after the
        firmware update.

        .. note:: This can take several minutes, don't abort it! If aborted,
                  the device stays in the bootloader and you need to restart
                  the update with ``emergency=True`` to recover.

        .. warning:: If the SEK-SensorBridge is connected through RS485
                     together with other SHDLC devices on the same bus, make
                     sure that no other device has the slave address 0 and
                     baudrate 115200! These connection settings are used by
                     the bootloader and thus two devices would respond to the
                     bootloader commands. If an update failes because of this,
                     you will have to disconnect the other device with address
                     0 and do an emergency update to recover this device.

        :param image: The image to flash, either as a
            :class:`~sensirion_shdlc_sensorbridge.firmware_image.SensorBridgeFirmwareImage`
            object, a file-like object, or the filename (``str``) to the
            \\*.hex file.
        :param bool emergency: Must be set to ``True`` if the device is already
                               in bootloader mode, ``False`` otherwise.
        :param callable status_callback: Optional callback for status report,
                                         taking a string as parameter.
        :param callable progress_callback: Optional callback for progress
                                           report, taking a float (progress in
                                           percent) as parameter.
        :raises ~sensirion_shdlc_driver.errors.ShdlcFirmwareImageIncompatibilityError:
            If the image is not compatible with the connected device.
        :raises Exception: On other errors.
        """  # noqa: E501
        if not isinstance(image, SensorBridgeFirmwareImage):
            image = SensorBridgeFirmwareImage(image)
        update = ShdlcFirmwareUpdate(self, image,
                                     status_callback=status_callback,
                                     progress_callback=progress_callback)
        update.execute(emergency=emergency)

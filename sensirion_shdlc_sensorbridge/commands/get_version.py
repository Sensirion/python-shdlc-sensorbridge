# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

##############################################################################
##############################################################################
#                 _____         _    _ _______ _____ ____  _   _
#                / ____|   /\  | |  | |__   __|_   _/ __ \| \ | |
#               | |       /  \ | |  | |  | |    | || |  | |  \| |
#               | |      / /\ \| |  | |  | |    | || |  | | . ` |
#               | |____ / ____ \ |__| |  | |   _| || |__| | |\  |
#                \_____/_/    \_\____/   |_|  |_____\____/|_| \_|
#
#     THIS FILE IS AUTOMATICALLY GENERATED AND MUST NOT BE EDITED MANUALLY!
#
# Generator:    sensirion-shdlc-interface-generator 0.5.1
# Product:      Sensor Bridge
# Version:      0.1.0
#
##############################################################################
##############################################################################

# flake8: noqa

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver.command import ShdlcCommand
from struct import pack, unpack

import logging
log = logging.getLogger(__name__)


class SensorBridgeCmdGetVersionBase(ShdlcCommand):
    """
    SHDLC command 0xD1: "Get Version".
    """

    def __init__(self, *args, **kwargs):
        super(SensorBridgeCmdGetVersionBase, self).__init__(
            0xD1, *args, **kwargs)


class SensorBridgeCmdGetVersion(SensorBridgeCmdGetVersionBase):

    def __init__(self):
        """
        Get Version Command

        Gets the version information for the hardware, firmware and SHDLC
        protocol.
        """
        super(SensorBridgeCmdGetVersion, self).__init__(
            data=[],
            max_response_time=0.005,
            post_processing_time=0.0,
            min_response_length=7,
            max_response_length=7
        )

    @staticmethod
    def interpret_response(data):
        """
        :return:
            - fw_ver_major (int) -
              Firmware major version number.
            - fw_ver_minor (int) -
              Firmware minor version number.
            - fw_debug (bool) -
              Firmware debug state. If the debug state is set, the firmware is
              in development.
            - hw_ver_major (int) -
              Hardware major version number.
            - hw_ver_minor (int) -
              Hardware minor version number.
            - protocol_ver_major (int) -
              Protocol major version number.
            - protocol_ver_minor (int) -
              Protocol minor version number.
        :rtype: tuple
        """
        fw_ver_major = int(unpack(">B", data[0:1])[0])  # uint8
        fw_ver_minor = int(unpack(">B", data[1:2])[0])  # uint8
        fw_debug = bool(unpack(">?", data[2:3])[0])  # bool
        hw_ver_major = int(unpack(">B", data[3:4])[0])  # uint8
        hw_ver_minor = int(unpack(">B", data[4:5])[0])  # uint8
        protocol_ver_major = int(unpack(">B", data[5:6])[0])  # uint8
        protocol_ver_minor = int(unpack(">B", data[6:7])[0])  # uint8
        return fw_ver_major,\
            fw_ver_minor,\
            fw_debug,\
            hw_ver_major,\
            hw_ver_minor,\
            protocol_ver_major,\
            protocol_ver_minor
# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.firmware_image import \
    SensorBridgeFirmwareImage
from sensirion_shdlc_driver.types import FirmwareVersion
import os


TESTS_ROOT = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(TESTS_ROOT, 'data')

EKS2_HEXFILE = os.path.join(DATA_DIR, 'Eks2_combined_V5.8.hex')
EKS2_PRODUCTTYPE = 0x00060000
EKS2_BL_MAJOR = 0
EKS2_BL_MINOR = 4
EKS2_APP_MAJOR = 5
EKS2_APP_MINOR = 8


def test_load_by_file_path():
    """
    Test if the image can be loaded by passing a filepath as string.
    """
    image = SensorBridgeFirmwareImage(EKS2_HEXFILE)
    assert image.size > 0


def test_load_by_file_object():
    """
    Test if the image can be loaded by passing a file-like object.
    """
    with open(EKS2_HEXFILE, mode='r') as f:
        image = SensorBridgeFirmwareImage(f)
        assert image.size > 0


def test_property_product_type():
    """
    Test if the value and type of the "product_type" property is correct.
    """
    image = SensorBridgeFirmwareImage(EKS2_HEXFILE)
    assert type(image.product_type) is int
    assert image.product_type == EKS2_PRODUCTTYPE


def test_property_bootloader_version():
    """
    Test if the value and type of the "bootloader_version" property is correct.
    """
    image = SensorBridgeFirmwareImage(EKS2_HEXFILE)
    assert type(image.bootloader_version) is FirmwareVersion
    assert image.bootloader_version.major == EKS2_BL_MAJOR
    assert image.bootloader_version.minor == EKS2_BL_MINOR
    assert image.bootloader_version.debug is False


def test_property_application_version():
    """
    Test if the value and type of the "application_version" property is
    correct.
    """
    image = SensorBridgeFirmwareImage(EKS2_HEXFILE)
    assert type(image.application_version) is FirmwareVersion
    assert image.application_version.major == EKS2_APP_MAJOR
    assert image.application_version.minor == EKS2_APP_MINOR
    assert image.application_version.debug is False

# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.firmware_image import \
    SensorBridgeFirmwareImage
import pytest
import os


TESTS_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_DIR = os.path.join(TESTS_ROOT, 'data')

EKS2_HEXFILE = os.path.join(DATA_DIR, 'Eks2_combined_V5.8.hex')


@pytest.mark.needs_device
def test_with_image(device):
    """
    Test if the update_firmware() function works when passing an
    SensorBridgeFirmwareImage object.
    """
    image = SensorBridgeFirmwareImage(EKS2_HEXFILE)
    result = device.update_firmware(image)
    assert result is None


@pytest.mark.needs_device
def test_with_file(device):
    """
    Test if the update_firmware() function works when passing a file-like
    object.
    """
    with open(EKS2_HEXFILE, mode='r') as f:
        result = device.update_firmware(f)
        assert result is None


@pytest.mark.needs_device
def test_with_filepath(device):
    """
    Test if the update_firmware() function works when passing a filepath.
    """
    result = device.update_firmware(EKS2_HEXFILE)
    assert result is None

# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if the serial number is returned properly.
    """
    serial_number = device.get_serial_number()
    assert type(serial_number) is str
    assert len(serial_number) == 24  # 24 hex chars = 12 bytes = 96 bit S/N
    assert int(serial_number, 16) > 0

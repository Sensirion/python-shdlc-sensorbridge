# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_sensorbridge.types import RepeatedTransceiveHandle


def test():
    """
    Test if the RepeatedTransceiveHandle object is properly constructed.
    """
    handle = RepeatedTransceiveHandle(13, 37)
    assert type(handle.raw_handle) is int
    assert handle.raw_handle == 13
    assert type(handle.rx_length) is int
    assert handle.rx_length == 37

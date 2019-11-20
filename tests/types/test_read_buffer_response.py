# -*- coding: utf-8 -*-
# (c) Copyright 2019 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
from sensirion_shdlc_driver.errors import ShdlcResponseError
from sensirion_shdlc_sensorbridge.types import ReadBufferResponse
import pytest


@pytest.mark.parametrize("rx_len,lost_bytes,remaining_bytes,rx_data,values", [
    (0, 0, 0, b"", []),
    (3, 4, 5, b"", []),
    (0, 0, 0, b"\x00\x01\x02", [
        (0x00, b""),
        (0x01, b""),
        (0x02, b""),
    ]),
    (2, 3, 4, b"\x00\x01\x02", [
        (0x00, b"\x01\x02"),
    ]),
    (2, 3, 4, b"\x00\x11\x22\x33\x44\x55\x66\x77\x88", [
        (0x00, b"\x11\x22"),
        (0x33, b"\x44\x55"),
        (0x66, b"\x77\x88"),
    ]),
])
def test_valid_data(rx_len, lost_bytes, remaining_bytes, rx_data, values):
    """
    Test if the ReadBufferResponse members are properly initialized when
    passing valid data.
    """
    resp = ReadBufferResponse(rx_len, lost_bytes, remaining_bytes, rx_data)
    assert type(resp.lost_bytes) is int
    assert resp.lost_bytes == lost_bytes
    assert type(resp.remaining_bytes) is int
    assert resp.remaining_bytes == remaining_bytes
    assert type(resp.values) is list
    assert [(v.raw_status, v.raw_data) for v in resp.values] == values


@pytest.mark.parametrize("rx_len,lost_bytes,remaining_bytes,rx_data", [
    (1, 2, 3, b"\x00"),
    (1, 2, 3, b"\x00\x11\x22"),
    (3, 2, 3, b"\x00"),
    (3, 2, 3, b"\x00\x11"),
    (3, 2, 3, b"\x00\x11\x22"),
    (3, 2, 3, b"\x00\x11\x22\x33\x44"),
    (3, 2, 3, b"\x00\x11\x22\x33\x44\x55"),
])
def test_invalid_data(rx_len, lost_bytes, remaining_bytes, rx_data):
    """
    Test if the ReadBufferResponse constructor raises an exception when
    passing invalid data.
    """
    with pytest.raises(ShdlcResponseError):
        ReadBufferResponse(rx_len, lost_bytes, remaining_bytes, rx_data)

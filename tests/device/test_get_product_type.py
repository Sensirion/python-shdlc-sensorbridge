# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test_without_args_returns_string(device):
    """
    Test if the product type is returned as string if no argument is passed.
    """
    product_type = device.get_product_type()
    assert type(product_type) is str
    assert product_type == "00060000"


@pytest.mark.needs_device
def test_as_int(device):
    """
    Test if the product type is returned as integer if as_int=True is passed.
    """
    product_type = device.get_product_type(as_int=True)
    assert type(product_type) is int
    assert product_type == 0x00060000

# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function
import pytest


@pytest.mark.needs_device
def test(device):
    """
    Test if the product name is returned properly.
    """
    product_name = device.get_product_name()
    assert type(product_name) is str
    assert product_name == "EKS2"

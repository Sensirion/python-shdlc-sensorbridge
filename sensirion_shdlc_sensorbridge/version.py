# -*- coding: utf-8 -*-
# (c) Copyright 2020 Sensirion AG, Switzerland

from __future__ import absolute_import, division, print_function

import importlib.metadata as metadata
from typing import Final

version: Final[str] = metadata.version("sensirion_shdlc_sensorbridge")

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Built-Ins
import os
import sys
import logging

from src.utils.logger import colorlevel


# Import Home-Grown
from . import ColorLevel



def get_logger(name: str, out=sys.stdout):
    handler = logging.StreamHandler(out)

    _logger = logging.Logger(name)
    formatter = colorlevel.ColorLevel
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    return _logger


# usage: logger = get_logger('NAME')



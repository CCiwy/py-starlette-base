#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Built-Ins
import sys
import logging

# Import Home-Grown
from . import colorlevel



def get_logger(name: str, out=sys.stdout):
    handler = logging.StreamHandler(out)

    _logger = logging.Logger(name)
    formatter = colorlevel.ColorLevel()
    handler.setFormatter(formatter)
    _logger.addHandler(handler)

    return _logger


# usage: logger = get_logger('NAME')

class LoggableMixin:
    def __init__(self):
        name = self.__class__.__name__
        self.logger = get_logger(name)



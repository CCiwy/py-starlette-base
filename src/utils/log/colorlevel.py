# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Import Built-Ins
import logging

# TODO: logger.info is not working: missing param record ?
from config.default import DEFAULT_LOG_FORMAT



class ColorLevel(logging.Formatter):

    # prefix/suffix
    RESET_SEQ = '\033[0m'
    COLOR_SEQ = '\033[1;%dm'
    BOLD_SEQ = '\033[1m'


    # color settings
    BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

    COLORS =  {
        'CRITICAL' : RED,
        'ERROR' : RED,
        'WARNING' : YELLOW,
        'DEBUG' : CYAN,
        'INFO' : WHITE,
        }


    # format settings -> todo: get from config
    err_fmt = '%(levelname)s %(asctime)s %(name)s[%(module)s.%(funcName)s(%(lineno)d)] %(message)s'
    dbg_fmt = '%(levelname)s %(asctime)s %(name)s[%(module)s.%(funcName)s(%(lineno)d)] %(message)s'
    info_fmt = '%(levelname)s %(asctime)s %(message)s'


    def __init__(self, fmt=DEFAULT_LOG_FORMAT):
        logging.Formatter.__init__(self, fmt)


    def format(self, record):
        levelno = record.levelno
        levelname = record.levelname
        
        levelname_color = ColorLevel.COLOR_SEQ % (30 + ColorLevel.COLORS[levelname]) + '[' + levelname + ']' + ColorLevel.RESET_SEQ

        record.levelname = levelname_color
        logging.Formatter.format(self, record)

        if levelno in [logging.DEBUG, logging.ERROR, logging.CRITICAL]:
            if not self._fmt == ColorLevel.dbg_fmt:
                logging.Formatter.__init__(self, ColorLevel.dbg_fmt)


        elif levelno in [logging.INFO, logging.WARNING]:
            if not self._fmt == ColorLevel.info_fmt:
                logging.Formatter.__init__(self, ColorLevel.info_fmt)

         
        result = logging.Formatter.format(self, record)
        return result

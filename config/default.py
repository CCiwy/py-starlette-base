# -*- coding: utf-8 -*-
#!/usr/bin/env python3.8

"""default settings"""

# Import Built-Ins
import os
import pathlib

from src.utils.log.filehandler import LOG_BACKUP_COUNT, TIME_ROTATING_WHEN

base_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
basedir = os.path.dirname(os.path.abspath(base_path))


# APP SETTINGS
APP_NAME = ''
SECRET_KEY = os.getenv('APP_SECRET')

# DB SETTINGS
DB_DRIVER = os.getenv('DB_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_LOCATION = os.getenv('DB_LOCATION')
DB_NAME = os.getenv('DB_NAME')
DB_CHARSET = os.getenv('DB_CHARSET')




MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_USER = os.getenv('MAIL_USER')
MAIL_PASS = os.getenv('MAIL_PASS')

ADMIN_MAIL = os.getenv('ADMIN_MAIL')

# LOGGER SETTINGS
LOG_DIR = os.path.join(basedir, './logs')
# create log dir if not exist
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

DEFAULT_LOG_FORMAT = '%(levelname)s %(asctime)s [%(module)s %(lineno)d] %(message)s'
TIME_ROTATING_WHEN = 'midnight'
LOG_BACKUP_COUNT = 7


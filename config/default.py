# -*- coding: utf-8 -*-
#!/usr/bin/env python3.8

"""default settings"""

# Import Built-Ins
import os
import pathlib

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

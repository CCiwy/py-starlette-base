from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
import logging


from src.utils.log.colorlevel import DEFAULT_FORMAT 

TIME_ROTATING_WHEN = 'midnight' # todo: get from conf
LOG_BACKUP_COUNT = 7 # todo: get from conf


def create_file_logger(app_name, log_dir):
    if not len(app_name):
        # app name not set in conf
        app_name = 'app'
    log_path = f'{log_dir}/{app_name.replace(" ", "_")}.log'
    file_handler = TimedRotatingFileHandler(
        log_path,
        when=TIME_ROTATING_WHEN,
        interval=1,
        backupCount=LOG_BACKUP_COUNT
    )


    file_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
    file_handler.setLevel(logging.DEBUG)

    # todo: identify streamhandler




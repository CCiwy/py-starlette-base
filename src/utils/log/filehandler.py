from logging import FileHandler
from logging.handlers import TimedRotatingFileHandler
import logging


from src.utils.log.colorlevel import DEFAULT_FORMAT 

TIME_ROTATING_WHEN = 'midnight' # todo: get from conf
LOG_BACKUP_COUNT = 7 # todo: get from conf


def create_file_logger(app):
    app_name = app.config.APP_NAME
    if not len(app_name):
        # app name not set in conf
        app_name = 'app'
    
    log_dir = app.config.LOG_DIR
    log_path = f'{log_dir}/{app_name.replace(" ", "_")}.log'
    
    time_rotate_when = app.config.TIME_ROTATING_WHEN
    log_backup_count = app.config.LOG_BACKUP_COUNT
    
    file_handler = TimedRotatingFileHandler(
        log_path,
        when=time_rotate_when,
        interval=1,
        backupCount=log_backup_count
    )


    _logger = logging.Logger(app_name)
    file_handler.setFormatter(logging.Formatter(DEFAULT_FORMAT))
    
    _logger.addHandler(file_handler)
    file_handler.setLevel(logging.INFO)

    
    return file_handler


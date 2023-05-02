#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Import Built-Ins
from typing import List
import os
import json

# Import Third-Party
from starlette.applications import Starlette

# Import Home-grown
from src.controllers import Controller # protocol
from src.database.session import AsyncSessionHandler
from src.database import create_table_if_not_exists

from src.errors import RequestError, DeserializeError

from src.utils.log import LoggableMixin
from src.utils.log.filehandler import create_file_logger


# CONFIG SETTINGS
APP_ENV = os.getenv("APP_ENV")
import config.default as settings
if APP_ENV == 'development':
    import config.development as config
else:
    import config.production as config


# ERROR HANDLING
DEFAULT_ERROR_MESSAGE = 'Something went wrong.'
def error_response(msg=DEFAULT_ERROR_MESSAGE, status=500):
    data = {'message' : msg} 
    return Response(json.dumps(data), status)


def report_error(error, request, message):
    """ not implemented yet. call mailer and send admin mail"""
    pass


def on_database_error(*args, **kwargs):
    request = args[0]
    error = args[1]
    # extract error message if we really want to

    
    report_error(error, request, 'database_error')
    return error_response()



def on_builtin_error(*args, **kwargs):
    request = args[0]
    error = args[1]

    report_error(error, request, 'database_error')
    return error_response()



def on_error(*args, **kwargs):
    request = args[0]
    error = args[1]
    status = error.status_code if hasattr(error.status_code) else 500
    return error_response(status=status)


class Backend(LoggableMixin, Starlette):
    db = False
    controllers = {}
    services = {}
    
    def __init__(self) -> None:
        self.config = config
        self.init_database()
        super(Backend, self).__init__()

        # init super before logger can be used!
        self.init_file_logger()
 
         

    def init_exception_handlers(self):
        # catch request based errors
        for exc in [RequestError, DeserializeError]:
            self.add_exception_handler(exc, on_error)

        # catch DB ERRORS

        # catch built errors [attrib, type...]
        for exc in [TypeError, AttributeError, KeyError]:
            self.add_exception_handler(exc, on_builtin_error)

    def init_controllers(self, controllers: List[Controller]) -> None:
        for ctrl_cls in controllers:
            self._init_controller(ctrl_cls)


    def _init_controller(self, ctrl_cls: Controller) -> None:
        ctrl = ctrl_cls(self)

        path_base, routes = ctrl.make_routes()
        for path_rel, methods, handler in routes:
            path = path_base + path_rel.rstrip("/")
            if not isinstance(methods, list):
                methods = [methods]
            self.logger.debug(f'{path} {handler}')
            self.add_route(path, handler, methods)

        self.controllers[ctrl.instance_name] = ctrl
        self.logger.debug(f'finished making routes for {self.instance_name}')


    def init_database(self):
        # todo: this is not failsave. improve config stuff!
        db_uri = self.config.SQLALCHEMY_DATABASE_URI
        self.db = AsyncSessionHandler(db_uri)


    def init_file_logger(self):
        create_file_logger(config.APP_NAME, settings.LOG_DIR)



    def init_event_handlers(self):
        self.add_event_handler("startup", self.on_app_start)
        self.add_event_handler("shutdown", self.on_app_stop)


    def init_services(self, services):
        if not self.db:
            self.logger.warn('no database connection established. can not init services')
            return

        for service_cls in services:
            self.services[service_cls.instance_name] = service_cls(self.db)


    def get_controller(self, ctrl_name):
        ctrl = self.controllers.get(ctrl_name, False)
        if ctrl:
            return ctrl

        self.logger.warn(f'controller {ctrl_name} not known!')


    def get_service(self, service_name):
        service = self.services.get(service_name, False)
        if service:
            return service

        self.logger.warning(f'service {service_name} not known!')


    async def on_app_start(self):
        if not self.db:
            self.logger.warning('no database connected')
            return
        create_table_if_not_exist(self.db)


    async def on_app_stop(self):
        pass


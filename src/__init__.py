#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Import Built-Ins
from typing import List
import os
import json

# Import Third-Party
from starlette.applications import Starlette
from starlette.middleware import Middleware

from starlette.responses import Response

from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware



# Import Home-grown
from src.controllers import Controller # protocol
from src.controllers import CONTROLLERS # list of controllers defined in module
from src.services import SERVICES
from src.database.session import AsyncSessionHandler
from src.database import create_table_if_not_exists
from src.configparser import Config
from src.exceptions import RequestError, DataBaseError, DeserializeError

from src.mailer import MailService

from src.utils.log import LoggableMixin, get_logger
from src.utils.log.filehandler import create_file_logger


APP_ENV = os.getenv("APP_ENV")


# ERROR HANDLING
DEFAULT_ERROR_MESSAGE = 'Something went wrong.'

class Backend(LoggableMixin, Starlette):
    db = False
    controllers = {}
    services = {}
    
    def __init__(self) -> None:

        context = Middleware(RawContextMiddleware,
                            plugins=(
                             plugins.RequestIdPlugin(),
                             plugins.CorrelationIdPlugin(),
                             plugins.UserAgentPlugin(),
                             ))

        self.config = Config('config')
        self.config.from_pyfile('default.py')
        self.config.from_pyfile(f'{APP_ENV}.py')


       

        self.init_database()
        Starlette.__init__(self, middleware=[context])
        super().__init__()

        # init super before logger can be used!
        self.init_file_logger()
        self.init_mailer()         

        self.init_controllers(CONTROLLERS)

        self.init_services(SERVICES)
        self.init_exception_handlers()

        self.logger.info(f'Application startup done. App name: {self.config.APP_NAME}') 

    
    # EXCEPTION HANDLING

    def error_response(self, msg=DEFAULT_ERROR_MESSAGE, status=500):
        data = {'message' : msg} 
        return Response(json.dumps(data), status)


    def report_error(self, error, request, message):
        """ call mailer and send admin mail"""
        if not self.config.DEBUG:
            self.mailer.send_error_mail(error, request, message)


    def on_database_error(self, *args, **kwargs):
        request = args[0]
        error = args[1]
        # extract error message if we really want to

        
        self.report_error(error, request, 'database_error')
        return self.error_response(msg='db error')



    def on_builtin_error(self, *args, **kwargs):
        request = args[0]
        error = args[1]
        
        self.logger.error(f'captured {error} in on_builtin_error')
        self.report_error(error, request, 'built in error')
        return self.error_response(msg="THIS IS WORKING")



    def on_error(self, *args, **kwargs):
        error = args[1]
        status = getattr(error, 'status', 500)
        msg = getattr(error, 'detail', DEFAULT_ERROR_MESSAGE)
        return self.error_response(msg=msg, status=status)


        
    def init_exception_handlers(self):
        # catch request based errors
        for exc in [RequestError, DeserializeError]:
            self.add_exception_handler(exc, self.on_error)

        # catch DB ERRORS
        for exc in [DataBaseError]:
            self.add_exception_handler(exc, self.on_database_error)

        # catch built errors [attrib, type...]
        for exc in [TypeError, AttributeError, KeyError]:
            self.add_exception_handler(exc, self.on_builtin_error)



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
        self.logger.debug(f'finished making routes for {ctrl.instance_name}')


    def init_database(self):
        db_uri = self.config.SQLALCHEMY_DATABASE_URI
        self.db = AsyncSessionHandler(db_uri)


    def init_file_logger(self):
        _filehandler = create_file_logger(self)
        self.logger.addHandler(_filehandler)
        

    def init_mailer(self):
        self.mailer = MailService(self, self.config.APP_NAME)
        


    def init_event_handlers(self):
        self.add_event_handler("startup", self.on_app_start)
        self.add_event_handler("shutdown", self.on_app_stop)


    def init_services(self, services):
        if not self.db:
            self.logger.warn('no database connection established. can not init services')
            return

        for service_cls in services:
            self.services[service_cls.instance_name] = service_cls(self.db)
            self.logger.debug(f'init services [{service_cls.instance_name}]')

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


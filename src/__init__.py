# Import Built-Ins
from typing import List

# Import Third-Party
from starlette.applications import Starlette

# Import Home-grown
from src.controllers import Controller # protocol

class Backend(Starlette):
    db = False
    controllers = {}
    services = {}
    
    def __init__(self) -> None:
        super(Backend, self).__init__()


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

            self.add_route(path, handler, methods)

        self.controllers[ctrl.instance_name] = ctrl


    def init_event_handlers(self):
        self.add_event_handler("startup", self.on_app_start)
        self.add_event_handler("shutdown", self.on_app_stop)


    def init_services(self, services):
        if not self.db:
            # todo: logger warn/use assert?
            return

        for service_cls in services:
            self.services[service_cls.instance_name] = service_cls(self.db)


    def get_controller(self, ctrl_name):
        ctrl = self.controllers.get(ctrl_name, False)
        if ctrl:
            return ctrl

        # todo: logger warn/raise exception?


    def get_service(self, service_name):
        service = self.services.get(service_name, False)
        if service:
            return service

        # todo: logger warn/raise exception?



    async def on_app_start(self):
        pass


    async def on_app_stop(self):
        pass


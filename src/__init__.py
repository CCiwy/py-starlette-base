from starlette.applications import Starlette


class Backend(Starlette):

    controllers = {}

    def __init__(self):
        super(Backend, self).__init__()



    def init_contollers(self, controllers):
        for ctrl_cls in controllers:
            self._init_controller(ctrl_cls)


    def _init_controller(self, ctrl_cls):
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
            self.services[service.instance_name] = service_cls(self.db)

    async def on_app_start(self):
        pass


    async def on_app_stop(self):
        pass


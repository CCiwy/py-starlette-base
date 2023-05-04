from src.controllers.base import BaseController

from src.utils.log.requests import request_logger
from src.utils.log.requests import RequestFlag

class DebugController(BaseController):
    instance_name = 'debug'
    


    def make_routes(self):
        path_base = '/debug'
        routes = [
            ("/", ["GET"], self.index),
            ("/error", ["GET"], self.trigger_error)
            ]

        return path_base, routes


    @request_logger(RequestFlag.BASE)
    async def index(self, request):
        return self.response('ok', 200)


    async def trigger_error(self, request):
        # this should break
        a = self.a
        return self.response('broken', 200)

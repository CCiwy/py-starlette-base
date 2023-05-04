# Import Home-Grown
from src.controllers.base import BaseController
from src.utils.log.requests import request_logger

class UserController(BaseController):

    instance_name = 'user'

    def make_routes(self):
        path_base = "/user"
        routes = []

        return path_base, routes

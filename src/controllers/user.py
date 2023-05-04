# Import Home-Grown
from typing import Required
from src.controllers.base import BaseController
from src.utils.log.requests import request_logger


from marshmallow.schema import Schema
from marshmallow.fields import String

class TokenRequestSchema(Schema):
    user_name = String(required=True)
    password = String(required=True)


class UserController(BaseController):

    instance_name = 'user'

    def make_routes(self):
        path_base = "/user"
        routes = []

        return path_base, routes


    async def get_token(self, request):
        token = 'asdf'
        return self.response(token, 200)

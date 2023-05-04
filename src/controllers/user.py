# Import Built-Ins
from typing import TYPE_CHECKING
# Import Third-Party
if TYPE_CHECKING:
   from marshmallow.schema import Schema


# Import Home-Grown
from src.controllers.base import BaseController
from src.schemas.user import TokenRequestSchema
from src.schemas.user import UserCreateSchema

from src.utils.log.requests import request_logger

# todo: move this to seperate file:
from enum import Enum

class UserError(str, Enum):
    AUTH_INCOMPLETE = 'Authdata incomplete'
    AUTH_INCORRECT = 'Authdata incorrect'
    NAME_NOT_FREE = 'Username is already in use'
    PASSWORDS_DONT_MATCH = 'Passwords dont match'
        
    def __repr__(self):
        return self.value





class UserController(BaseController):

    instance_name = 'user'

    def make_routes(self):
        path_base = "/user"
        routes = [
            ("/token", "POST", self.get_token),
            ("/create", "POST", self.create_user)
        ]

        return path_base, routes

    async def create_user(self, request):
        data = await self.deserialize_request(request, schema=UserCreateSchema)
        
        user_name = data.get('user_name')
        password = data.get('password')
        password_repeat = data.get('password_repeat')

        if not (user_name and password and password_repeat):
            # should never happen without request deserialize error
            #return self.bad_request(UserError.AUTH_INCOMPLETE)
            return self.response(UserError.AUTH_INCOMPLETE, 403)


        if not password == password_repeat:
            return self.response(UserError.PASSWORDS_DONT_MATCH, 403)
        

        user_service = self.app.get_service("user")

        user_exists =  user_service.get_user("user_name")
        if user_exists:
            # check what status code is the proper one to return here
            return self.response(UserError.NAME_NOT_FREE, 403)

        user_service.create_user(user_name, password)
       

        return self.response('Account created', 201)

    @request_logger('base')
    async def get_token(self, request):
        # deserialize request
        data = await self.deserialize_request(request, schema=TokenRequestSchema)
        user_name = data.get('user_name')
        password = data.get('password')
        if not (user_name and password):
            # should never happen without request deserialize error
            #return self.bad_request(UserError.AUTH_INCOMPLETE)
        
            return self.response(UserError.AUTH_INCOMPLETE, 403)

        # call user_service
        user_service = self.app.get_service("user")
        user_model = user_service.get_user(user_name)
        # check if user exist + password matches
        if not user_model or not user_service.verifiy_password(user_model, password):
            return self.response(UserError.AUTH_INCORRECT, 403)
            #return self.unauthorized(UserError.AUTH_INCORRECT) 
        # todo: this will be async methods after implementing service correctly
    
        # start session, get token
        token = user_model.start_session()

        return self.response(token, 200)

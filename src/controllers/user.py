# Import Built-Ins
from typing import TYPE_CHECKING

# Import Third-Party
if TYPE_CHECKING:
   from marshmallow.schema import Schema


# Import Home-Grown
from src.controllers.base import BaseController
from src.database.session import DBResult, DBStatus

from src.error_codes import UserError

from src.schemas.user import TokenRequestSchema
from src.schemas.user import UserCreateSchema
from src.schemas.user import UserProfileSchema

from src.utils.auth import authenticated

from src.utils.log.requests import request_logger
from src.utils.log import get_logger
logger = get_logger('CTRL')


class UserController(BaseController):

    instance_name = 'user'

    def make_routes(self):
        path_base = "/user"
        routes = [
            ("/token", "POST", self.get_token),
            ("/create", "POST", self.create_user),
            ("/profile", "GET", self.my_user_data)
        ]

        return path_base, routes


    #@request_logger('base')
    async def create_user(self, request):
        data = await self.deserialize_request(request, schema=UserCreateSchema)
        user_name = data.get('user_name')
        password = data.get('password')
        password_repeat = data.get('password_repeat')

        if not (user_name and password and password_repeat):
            # should never happen without request deserialize error
            #return self.bad_request(UserError.AUTH_INCOMPLETE)
            return self.bad_request(UserError.AUTH_INCOMPLETE)


        if not password == password_repeat:
            return self.bad_request(UserError.PASSWORDS_DONT_MATCH)
        

        user_service = self.app.get_service("user")

        
        user_exists = await user_service.user_exists(user_name)
        if user_exists:
            # check what status code is the proper one to return here
            return self.bad_request(UserError.USER_ALREAD_EXISTS)

        result = await user_service.create_user(user_name, password)

        if not result.status == DBStatus.OK:
            return self.internal_error('sth went wrong')
       

        return self.response('Account created', 201)


    #@request_logger('base')
    async def get_token(self, request):
        # deserialize request
        data = await self.deserialize_request(request, schema=TokenRequestSchema)
        user_name = data.get('user_name')
        password = data.get('password')
        if not (user_name and password):
            # should never happen without request deserialize error
            return self.bad_request(UserError.AUTH_INCOMPLETE)
        

        # call user_service
        user_service = self.app.get_service("user")
        user_result = await user_service.get_user(user_name)
        if not user_result.status == DBStatus.OK:
            return self.unauthorized(UserError.AUTH_INCORRECT)

        user_model = user_result.data
        # check if user exist + password matches
        if not user_model or not user_model.verifiy_password(password):
            return self.unauthorized(UserError.AUTH_INCORRECT) 
    
        # start session, get token
        token = await user_service.start_session(user_model.uuid)

        return self.response(token, 200)


    @request_logger('base')
    @authenticated('base')
    async def my_user_data(self, request, user=False):

        logger.debug(f'USER: {user}')
        if not user:
            return self.unauthorized('not authenticated')

        logger.debug('should call json response')
        return self.json_response(data=user, schema=UserProfileSchema, status=200)



# Import Third-Party
from marshmallow.schema import Schema
from marshmallow.fields import String


# Import Home-Grown
from src.controllers.base import BaseController
from src.utils.log.requests import request_logger


# todo: move this to seperate file:
from enum import Enum

class UserError(Enum):
    AUTH_INCOMPLETE = 'Authdata incomplete'
    AUTH_INCORRECT = 'Authdata incorrect'

class TokenRequestSchema(Schema):
    user_name = String(required=True)
    password = String(required=True)



def hash_password(password):
    # todo: implement this
    return password

def create_token():
    return 'asdf'

class UserModel:
    # todo: create this as Basemodel instance
    def __init__(self, name, password):
        self.name = name
        self.salted_pass = hash_password(password)
        self.token = False # delete after implementing as BaseModel


    def start_session(self):
        self.token = create_token()
        # add expiration timer
        return self.token

class UserService:

    def __init__(self):
        self.users = dict()
        
    def verifiy_password(self, user: UserModel, password: str) -> bool:
        hashed = hash_password(password)
        return hashed == user.salted_pass


    def get_user(self, user_name):
        return self.users.get('user_name', False)



    def create_user(self, user_name, password):
        self.users[user_name] = UserModel(user_name, password)



userservice = UserService()
userservice.create_user('ciwy', 'pass')

class UserController(BaseController):

    instance_name = 'user'

    def make_routes(self):
        path_base = "/user"
        routes = [
            ("/token", "POST", self.get_token)
        ]

        return path_base, routes


    async def get_token(self, request):
        # deserialize request

        data = await self.deserialize_request(request, schema=TokenRequestSchema)
        user_name = data.get('user_name')
        password = data.get('password')
        if not user_name and password:
            # should never happen without request deserialize error
            #return self.bad_request(UserError.AUTH_INCOMPLETE)
        
            return self.response(UserError.AUTH_INCOMPLETE, 403)


        # call userservice
        user_model = userservice.get(user)

        # check if user exist + password matches
        if not user_model or not userservice.verifiy_password(user_model, password):
            return self.response(UserError.AUTH_INCORRECT, 403)
            #return self.unauthorized(UserError.AUTH_INCORRECT) 
        # todo: this will be async methods after implementing service correctly
    
        # start session, get token
        token = user_model.start_session()

        return self.response(token, 200)

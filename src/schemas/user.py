from marshmallow.schema import Schema
from marshmallow.fields import String


class UserCreateSchema(Schema):
    user_name = String(required=True)
    password = String(required=True)
    password_repeat = String(required=True)



class TokenRequestSchema(Schema):
    user_name = String(required=True)
    password = String(required=True)



class UserProfileSchema(Schema):
    user_name = String()
    

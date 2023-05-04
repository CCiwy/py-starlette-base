from marshmallow.schema import Schema
from marshmallow.fields import String

class TokenRequestSchema(Schema):
    user_name = String(required=True)
    password = String(required=True)

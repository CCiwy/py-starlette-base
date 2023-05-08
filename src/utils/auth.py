# Import Built-Ins
from functools import wraps

# Import Third-Party
from jose import jwt
from jose.exceptions import JWTError

JWT_ALGO = 'HS256'
TOKEN_SECRET = 'secret'  # todo: get from app config, maybe make sure its not equal to app secret
TOKEN_TYPE = 'x-api-token' # todo: check hot this works with templates


def generate_auth_token(uuid, token_type=TOKEN_TYPE):
    to_encode = {
        'token_type' : token_type,
        'uuid' : uuid
    }

    token = jwt.encode(
        to_encode,
        TOKEN_SECRET,
        algorithm=JWT_ALGO
    )

    return token

def decode_auth_token(token):
    try:
        payload = jwt.decode(
                    token,
                    TOKEN_SECRET,
                    algorithms=[JWT_ALGO]
                    )
        uuid = payload.get('uuid')
        return uuid, token

    except JWTError:
        return False


def resolve_auth_data(auth_data):
    _, token = auth_data.split(":")

    user_data = decode_auth_token(token)

    return user_data


# async def authenticated(drole):
def authenticated(auth_type):
    def auth_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            controller = args[0]

            request = args[1]

            user_getter = controller.app.get_service('user').get_by_uuid
            # user_getter = await controller.app.get_service('user').get_by_uuid
            user = False

            auth_data = request.headers.get('Authorization', False)
            
            if not auth_data:
                # no authentication in request headers 
                return False

            user_data = resolve_auth_data(auth_data)
            
            if not user_data:
                return False

            uuid, token = user_data


            # todo: use db result after implemented
            user = await user_getter.get_by_uuid(uuid)

            if not (user and user.token == token):
                return False

            return user



            return await func(*args, **kwargs)
        return wrapper
    return auth_decorator


# Import Built-Ins
from functools import wraps

# Import Third-Party
from jose import jwt
from jose.exceptions import JWTError

from src.exceptions import Unauthorized

from src.database.session import DBStatus
from src.error_codes import UserError


JWT_ALGO = 'HS256'
TOKEN_SECRET = 'secret'  # todo: get from app config, maybe make sure its not equal to app secret
TOKEN_TYPE = 'x-api-token' # todo: check hot this works with templates


from src.utils.log import get_logger

logger = get_logger('auth')

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


def resolve_auth_data(token):
    user_data = decode_auth_token(token)

    return user_data


def authenticated(auth_type):
    def auth_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            controller = args[0]

            request = args[1]

            user_getter = controller.app.get_service('user').get_by_uuid
            user = False

            auth_data = request.headers.get('Authorization', False)
            
            if not auth_data:
                # no authentication in request headers 
                raise Unauthorized(UserError.AUTH_INCOMPLETE)

            user_data = resolve_auth_data(auth_data)
            if not user_data:
                raise Unauthorized(UserError.AUTH_INCORRECT)

            uuid, token = user_data


            user_result = await user_getter(uuid)
            user = user_result.data if user_result.status == DBStatus.OK else False
            
            if not (user and user.token == token):
                raise Unauthorized(UserError.SESSION_EXPIRED)

            return await func(*args, user=user,**kwargs)
        return wrapper
    return auth_decorator


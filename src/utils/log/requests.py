#  Import Built-Ins
from functools import wraps
from enum import Enum, auto

# Import Third-Party
from starlette_context import context


# Import Home-Grown
from src.utils.log.logger import get_logger

# Note: import app_env or debug to see if request logging is needed

logger = get_logger('[REQUEST]')

class RequestFlag(Enum):
    BASE = auto()
    FULL = auto()




def request_logger(flag):
    def request_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            controller = args[0]
            cname = controller.instance_name
            request_id = context.data.get('X-Request-ID')
            correlation_id = context.data.get('X-Correlation-ID')
            user_agent = context.data.get('User-Agent')
            logger.info(f'[{correlation_id}] EP: {cname}.{func.__name__}')
            logger.info(f'[{correlation_id}] request-id: {request_id}')
            logger.info(f'[{correlation_id}] header: {user_agent}')

            #if flag == RequestFlag.FULL:
                # do more stuff here?
                
            return await func(*args, **kwargs)
        return wrapper
    return request_decorator


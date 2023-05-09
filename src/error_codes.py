from enum import Enum


class ErrorCode(str, Enum):
    def __repr__(self):
        return self.value



class BackendError(ErrorCode):
    DEFAULT = 'Something went wrong'


# todo: write tests for these
class UserError(ErrorCode):
    PASSWORDS_DONT_MATCH = 'passwords dont match'
    AUTH_INCOMPLETE = 'authdata incomplete'
    AUTH_INCORRECT = 'authdata incorrect'
    USER_ALREAD_EXISTS = 'user already exists'
    SESSION_EXPIRED = 'session expired' 

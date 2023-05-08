from enum import Enum


class ErrorCode(str, Enum):
    def __repr__(self):
        return self.value



class BackendError(ErrorCode):
    DEFAULT = 'Something went wrong'



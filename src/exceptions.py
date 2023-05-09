class ErrorBase(RuntimeError):

    def __init__(self, detail='', source=None):
        self.detail = detail
        self.source = detail

    @classmethod
    def init_from(cls, error):
        detail = getattr(error, 'message', repr(error))
        return cls(detail)


    def __repr__(self):
        return f'{self.__class__.__name__} {self.detail}'


class RequestError(ErrorBase):
    pass


class Unauthorized(RequestError):
    status = 403


class DeserializeError(ErrorBase):
    status = 400


class DataBaseError(ErrorBase):
    status = 500


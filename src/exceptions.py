class RequestError(RuntimeError):
    pass


class Unauthorized(RequestError):
    status = 403

class DeserializeError(RuntimeError):
    status = 400
    @classmethod
    def init_from(cls, error):
        detail = getattr(error, 'message', repr(error))
        return cls(detail)


class DataBaseError(RuntimeError):
    pass


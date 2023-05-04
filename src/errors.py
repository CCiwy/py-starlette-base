class RequestError(RuntimeError):
    pass


class DeserializeError(RuntimeError):
    @classmethod
    def init_from(cls, error):
        detail = getattr(error, 'message', repr(error))
        return cls(detail)


class DataBaseError(RuntimeError):
    pass


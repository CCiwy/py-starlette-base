""" database basemodel declaration """
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseModel:
    __mapper_args__ = {'eager_defaults' : True}


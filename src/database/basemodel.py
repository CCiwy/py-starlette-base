""" database basemodel declaration """
from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    __mapper_args__ = {'eager_defaults' : True}


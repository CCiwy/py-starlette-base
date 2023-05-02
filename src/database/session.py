""" module for database managment using sqlalchemy Async Engine"""
# Import Built-Ins
from enum import Enum, auto
from typing import Any


# Import Third-Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


# Import Home-Grown
from src.database.basemodel import BaseModel

class DatabaseError(RuntimeError):
    """ generic db error """
    pass

class DBStatus(Enum):
    OK = auto()
    ERROR = auto()
    UPDATE = auto()
    DELETE = auto()


class DBResult:
    # depends on query, most likeley db-model instance
    # but possible are multiple rows, partial results or an Error
    def __init__(self, status, data=None) -> None:
        self.status = status
        self.data = data

class AsyncSessionHandler:

    def __init__(self, uri: str, echo=False) -> None:
        self.uri = uri
        self.engine = create_async_engine(self.uri, echo=echo, pool_pre_ping=True)
        self._session = sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)


    @property
    def session(self):
        return self._session()


    async def __aenter__(self) -> AsyncSession:
        """ async routine, enables using async session as context """
        return self.make_session()


    async def __aexit__(self, *args, **kwargs) -> Any:
        """ async routine, enable closing of async context """
        return self.__exit__(*args, **kwargs)



class DatabaseService:
    """ service layer for database connections """
    def __init__(self, db):
        self.db = db


    # methods to ensure database results/errors are encapsulated
    
    def _status_ok(self, data=None):
        return DBResult(DBStatus.OK, data=data)


    def _status_error(self, error):
        return DBResult(DBStatus.ERROR, data=error)


    def _update_ok(self, model):
        return DBResult(DBStatus.UPDATE, data=model)


    def _delete_okay(self, id):
        return DBResult(DBStatus.DELETE, id)

""" module for database managment. Using sqlalchemy Async Engine"""

# Import Built-Ins
from dataclasses import dataclass
from enum import Enum, auto
from typing import Union


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


@dataclass
class DBResult:
    status = DBStatus
    data = Union[BaseModel, DatabaseError]
        

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





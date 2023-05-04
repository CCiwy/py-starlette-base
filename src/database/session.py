""" module for database managment using sqlalchemy Async Engine"""
# Import Built-Ins
from enum import Enum, auto
from typing import Any


# Import Third-Party
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


from sqlalchemy import select, update, delete

# Import Home-Grown
from src.database.basemodel import BaseModel
from src.errors import DataBaseError


class LookUpError(DataBaseError):
    def __init__(self, source, message):
        self.source = source
        self.message = message


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

    async def save(self, model):
        async with self.db.session as session:
            async with session.begin():
                try:
                    session.add(model)
                    return self._status_ok()
                except AttributeError as e:
                    await session.rollback()
                    return self._status_error(e)


    async def get_by_id(self, id):
        stmt = select(self._model).where(self._model.id==id)
        async with self.db.session as session:
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return self._status_error(LookUpError(self.instance_name, id))
            return self._status_ok(model)


    async def get_all(self):
        stmt = select(self._model)
        async with self.db.session as session:
            result = await session.execute(stmt)
            rows = result.scalars().all()

            if not rows:
                rows = []
                
            return self._status_ok(rows)


    async def update_by_id(self, id, **kwargs):
        stmt = update(self._model).\
                    where(self._model.id == id).\
                    values(**kwargs).\
                    execution_options(synchronize_session='fetch')

        async with self.db.session as session:
            model = await session.execute(stmt)
            await session.commit()
            return self._update_ok(model)


    async def delete_by_id(self, id):
        """ todo: cant cascade """
        stmt = delete(self._model).where(self._model.id==id)
        async with self.db.session as session:
            await session.execute(stmt)
            return self._delete_okay(id)


    # methods to ensure database results/errors are encapsulated
    def _status_ok(self, data=None):
        return DBResult(DBStatus.OK, data=data)


    def _status_error(self, error):
        return DBResult(DBStatus.ERROR, data=error)


    def _update_ok(self, model):
        return DBResult(DBStatus.UPDATE, data=model)


    def _delete_okay(self, id):
        return DBResult(DBStatus.DELETE, id)

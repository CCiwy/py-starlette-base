# Import Built-Ins


# Import Third-Party
from sqlalchemy import select
from sqlalchemy.sql.functions import user


# Import Home-Grown
from src.database.session import DatabaseService
from src.database.session import LookUpError


from src.database.models.user import UserModel

class UserService(DatabaseService):
    instance_name = 'user'
    _model = UserModel


    async def get_by_uuid(self, uuid):
        stmt = select(self._model).where(self._model.uuid == uuid)
        async with self.db.session as session:
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            if model is None:
                return self._status_error(LookUpError(uuid, self.instance_name))
            

            return self._status_ok(model)


    async def start_session(self, uuid):
        stmt = select(self._model).where(self._model.uuid == uuid)

        async with self.db.session as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                return

            token = user.start_session()
            await session.commit()
            return token

    async def user_exists(self, user_name):
        user = await self._get_user(user_name)
        return user is not None


    async def get_user(self, user_name):
        model = await self._get_user(user_name)
        if model is None:
            return self._status_error(LookUpError(user_name, self.instance_name))

        return model


    async def _get_user(self, user_name): 
        stmt = select(self._model).where(self._model.name == user_name)
        async with self.db.session as session:
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()
            return model


    async def create_user(self, user_name, password):
        user_model = UserModel(user_name, password)

        return await self.save(user_model)



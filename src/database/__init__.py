from src.database.basemodel import BaseModel


async def create_table_if_not_exists(db):
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)


async def db_reset(db):
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

# Import Built-Ins
import unittest
import asyncio

# Import Third-Party
from starlette.testclient import TestClient

from sqlalchemy import Column, Integer, String
from sqlalchemy import select


# Import Home-Grown
from src import Backend

from src.database.session import DatabaseService
from src.database.basemodel import BaseModel
from src.database import db_reset

from src.database.session import DBResult, DBStatus

app = Backend()

class ExampleModel(BaseModel):
    __tablename__ = 'example'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)


    def __init__(self, name: str) -> None:
        self.name = name


class ExampleService(DatabaseService):
    instance_name = 'example'
    _model = ExampleModel
    
                   


class DataBaseServiceTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app = app
        self.client = TestClient(self.app)
       

    def tearDown(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db_reset(self.app.db))



    def test_example_service_init(self):
        services = [ExampleService]
        self.app.init_services(services)
        self.assertTrue(ExampleService.instance_name in self.app.services)

class DataBaseTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.app = app
        self.client = TestClient(self.app)
       
        services = [ExampleService]
        self.app.init_services(services)

    def tearDown(self) -> None:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db_reset(self.app.db))




    async def test_example_service_save_model_returns_db_status_ok(self):
        model = ExampleModel("name")
        service = self.app.get_service("example")

        result = await service.save(model)
        self.assertEqual(result.status, DBStatus.OK)



    async def test_example_service_get_model_returns_db_status_ok(self):
        name = "ExampleName"
        model = ExampleModel(name)
        
        service = self.app.get_service("example")
        _ = await service.save(model)

        result = await service.get_by_id(1)
        self.assertEqual(result.status, DBStatus.OK)


    async def test_example_service_get_model_returns_saved_model(self):
        name = "ExampleName"
        model = ExampleModel(name)
        service = self.app.get_service("example")
        _ = await service.save(model)

        result = await service.get_by_id(1)
        self.assertEqual(result.data.name, name)


    
    async def test_example_service_delete_model(self):
        name = "ExampleName"
        model = ExampleModel(name)
        service = self.app.get_service("example")
        _ = await service.save(model)

        result = await service.delete_by_id(1)
        self.assertEqual(result.status, DBStatus.DELETE)



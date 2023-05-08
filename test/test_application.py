import unittest

from starlette.testclient import TestClient


from src import Backend
from src.controllers.base import BaseController

app = Backend()

class ExampleController(BaseController):
    instance_name = 'example'

    def make_routes(self):
        path_base = '/example'
        routes = [
            ('/', "GET", self.index)
        ]

        return path_base, routes

    def index(self, request):
        return self.response('ok',200)

class ApplicationTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.app = app
        self.client = TestClient(self.app)

    def tearDown(self):
        pass


    def test_application_running(self):
        self.assertTrue(self.app)


    def test_init_example_controller(self):
        controllers = [ExampleController]
        self.app.init_controllers(controllers)

        self.assertTrue(ExampleController.instance_name in self.app.controllers)
        

    def test_example_controller_index_returns_status_200(self):
        controllers = [ExampleController]
        self.app.init_controllers(controllers)

        response = self.client.get("/example/")
        self.assertEqual(response.status_code, 200)


    def test_example_controller_index_returns_msg_ok(self):
        controllers = [ExampleController]
        self.app.init_controllers(controllers)

        response = self.client.get("/example/")
        self.assertEqual(response._content.decode("utf-8"), "ok")


    def test_example_controller_non_existing_route_returns_status_404(self):

        controllers = [ExampleController]
        self.app.init_controllers(controllers)

        response = self.client.get("/example/non_existing")
        self.assertEqual(response.status_code, 404)






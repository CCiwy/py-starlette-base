from unittest import IsolatedAsyncioTestCase
import json
import asyncio

from starlette.testclient import TestClient

from src import Backend
from src.controllers.base import BaseController

from src.utils.auth import authenticated
from src.database import db_reset
app = Backend()


TEST_USER = 'TestUser'
TEST_PASS = 'testpass'

def create_valid_user_data():
    data = {
            'user_name' : TEST_USER,
            'password' : TEST_PASS,
            'password_repeat' : TEST_PASS,
    }
    return json.dumps(data)

def create_account(client):
    url = '/user/create/'
    data = create_valid_user_data()

    json_data = json.dumps(data)
    client.post(url=url, data=json_data)


class AuthController(BaseController):

    instance_name = 'auth'

    def make_routes(self):
        path_base = '/auth'

        routes = [
            ('/', 'GET', self.index),
            ('/auth/', 'GET', self.needs_auth)   
            ]

        return path_base, routes



    async def index(self, request):
        return self.response('ok', 200)


    @authenticated('base')
    async def needs_auth(self, request, user=False):
        return self.response('ok', 200)


class TestAuth(IsolatedAsyncioTestCase):

    def setUp(self):
        self.app = app
        self.client = TestClient(self.app)
        self.app.init_controllers([AuthController])
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(db_reset(self.app.db))



    async def test_controller_index_return_status_is_200(self):
        """ make sure controller is inited """
        url = '/auth/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


    def test_controller_auth_without_user_returns_403(self):
        url = '/auth/auth'
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, 403)



    async def test_controller_auth_with_user_returns_200(self):
        # create account + get token
        json_data = create_valid_user_data()

        create_response = self.client.post(url='/user/create/', data=json_data)

        self.assertEqual(create_response.status_code, 201)
        response = self.client.post(url='/user/token/', data=json_data)
        self.assertEqual(response.status_code, 200)

        token = response._content.decode('UTF-8') 
        # actual test
        url = '/auth/auth'
        
        auth_header = {"content-type": "application/json; charset=UTF-8","Authorization": token}
        response = self.client.get(url=url, headers=auth_header)
        self.assertEqual(response.status_code, 200)

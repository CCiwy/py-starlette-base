from unittest import IsolatedAsyncioTestCase
import asyncio
import json

from starlette.testclient import TestClient

from src import Backend

from src.database import db_reset
from src.error_codes import UserError

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



class TestUserController(IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.app = app

        self.client = TestClient(self.app)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(db_reset(self.app.db))

        #loop.run_until_complete(create_table_if_not_exists(self.app.db))

        self.controller = self.app.get_controller('user')


    def test_create_user_with_valid_data_returns_status_201(self):
        json_data = create_valid_user_data()
        url = '/user/create'

        response = self.client.post(url, data=json_data)

        self.assertEqual(response.status_code, 201)


    def test_create_user_without_password_repeat_returns_status_400(self):
        json_data = json.dumps({"user_name" : TEST_USER, "password" : TEST_PASS})
        url = '/user/create'

        response = self.client.post(url, data=json_data)

        self.assertEqual(response.status_code, 400)


    def test_create_user_returns_data_msg_is_account_created(self):
        json_data = create_valid_user_data()
        url = '/user/create'

        response = self.client.post(url, data=json_data)

        _data = response._content.decode('UTF-8') 

        self.assertTrue('Account created' in _data)



    def test_token_with_valid_data_statuscode_is_200(self):
        json_data = create_valid_user_data()
        create_url = '/user/create'
        _ = self.client.post(url=create_url, data=json_data)

        token_url = '/user/token'

        token_response = self.client.post(url=token_url, data=json_data)

        self.assertEqual(token_response.status_code, 200)


    def test_token_with_incomplete_data_statuscode_is_400(self):
        json_data = create_valid_user_data()
        create_url = '/user/create'
        _ = self.client.post(url=create_url, data=json_data)

        token_url = '/user/token'
        invalid_data = json.dumps({"user_name" : TEST_USER})

        token_response = self.client.post(url=token_url, data=invalid_data)

        self.assertEqual(token_response.status_code, 400)



    def test_token_with_invalid_data_statuscode_is_403(self):
        json_data = create_valid_user_data()
        create_url = '/user/create'
        _ = self.client.post(url=create_url, data=json_data)

        token_url = '/user/token'
        invalid_data = json.dumps({"user_name" : TEST_USER, "password" : "wrong"})

        token_response = self.client.post(url=token_url, data=invalid_data)

        self.assertEqual(token_response.status_code, 403)



    def test_user_request_token_response_data_is_str(self):
        json_data = create_valid_user_data()
        create_url = '/user/create'
        _ = self.client.post(url=create_url, data=json_data)

        token_url = '/user/token'

        token_response = self.client.post(url=token_url, data=json_data)

        token = token_response._content.decode('UTF-8')

        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)

        
    def test_authenticated_route_with_correct_token_returns_status_200(self):
        json_data = create_valid_user_data()
        create_url = '/user/create'
        _ = self.client.post(url=create_url, data=json_data)

        token_url = '/user/token'

        token_response = self.client.post(url=token_url, data=json_data)

        token = token_response._content.decode('UTF-8')

        profile_url = '/user/profile'

        auth_header = {"content-type": "application/json; charset=UTF-8","Authorization": token}

        response = self.client.get(url=profile_url, headers=auth_header)
        
        self.assertEqual(response.status_code, 200)
        

    def test_authenticated_route_without_token_returns_403(self):
        profile_url = '/user/profile'
        response = self.client.get(profile_url)
        self.assertEqual(response.status_code, 403)


    def test_authenticated_route_with_incorrect_token_returns_msg_is_auth_incorrect(self):
        profile_url = '/user/profile'

        auth_header = {"content-type": "application/json; charset=UTF-8","Authorization": 'token'}

        response = self.client.get(url=profile_url, headers=auth_header)
        

        response_data = response._content.decode('UTF-8')
        response_json = json.loads(response_data)
        response_message = response_json["message"]

        self.assertEqual(response_message, UserError.AUTH_INCORRECT)
        


    def test_authenticated_route_with_incorrect_token_returns_status_403(self):
        profile_url = '/user/profile'

        auth_header = {"content-type": "application/json; charset=UTF-8","Authorization": 'token'}

        response = self.client.get(url=profile_url, headers=auth_header)
        
        self.assertEqual(response.status_code, 403)
        

import os
import sys
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('../')

from app import app, login_manager
from models import User, Base
from dbSession import session as _session, engine

class TestCase(unittest.TestCase):
    clean_up    = True
    session     = _session
    app = []
    def setUp(self):
        app.config['TESTING'] = True
        app.secret_key="Something"
        self.app = app.test_client()
        login_manager.init_app(app)
        login_manager.login_view = 'login_api.login'

    def tearDown(self):
        if self.clean_up:
            self.session.query(User).delete()
            self.session.commit()
            self.session.close()

    def tearDownClass():
        os.remove('finalProject.db')

    def does_url_response_contain_substring(self ,url, sub_string):
        response = self.app.get(url, follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue(self.does_data_contain_substring(response.data, sub_string))

    def does_data_contain_substring(self, in_data, sub_string):
        data = str(in_data)
        if sub_string is not str:
            sub_string = str(sub_string)
        if sub_string in data:
            return True
        else:
            return False

    def create_minimal_user(self, user_name, password):
        new_user = User(user_name=user_name, email='something@google.com')
        new_user.generate_api_key()
        new_user.hash_password(password)
        self.session.add(new_user)
        self.session.commit()

    def login_user(self, user, pw):
        response = self.app.post('/login', data=dict(username=user, password=pw), follow_redirects=True)
        self.assertEqual(response.status_code,200)

    def logout_user(self):
        response = self.app.get('logout')
        self.assertEqual(response.status_code,200)

    def test_get_login_route(self):
        self.does_url_response_contain_substring( '/login', r'<title>Login</title>')

    def test_get_index_page(self):
        self.does_url_response_contain_substring( '/', r'<title>Meet\'N eat</title>')

    def test_get_apiKey_page_whitout_logged_in_user(self):
        self.does_url_response_contain_substring( '/apiKey', r'<title>Login</title>')

    def test_get_logout_page_whitout_logged_in_user(self):
        self.does_url_response_contain_substring( '/logout', r'<title>Login</title>')

    def test_post_request_with_wrong_password(self):
        user_name = 'Nawin'
        pw = 'something'
        self.create_minimal_user(user_name,pw)
        response = self.app.post('/login', data=dict(username=user_name, password='qweq'), follow_redirects=True)
        self.assertEqual(response.status_code,200)
        self.assertTrue(self.does_data_contain_substring(response.data,r'<strong>Error!</strong> Invalid Credentials\n'))

    def test_post_request_with_correct_password(self):
        user_name = 'Nawin'
        pw = '1234'
        self.create_minimal_user(user_name, pw)
        response = self.app.post('/login', data=dict(username=user_name, password=pw), follow_redirects=True)
        self.assertEqual(response.status_code,200)
        if response.is_json:
            self.assertNotEqual(response.get_json().get('token'),None)
        else:
            self.assertTrue(False)

    def test_token_route_no_key(self):
        result = self.app.get('/token_route')
        self.assertEqual(result.status_code, 401)

    def test_token_route_false_key(self):
        result = self.app.get('/token_route',query_string=dict(token='asda'))
        self.assertEqual(result.status_code,401)

    def test_token_route_with_valid_token(self):
        self.create_minimal_user('Nawin','abcd')
        self.login_user('Nawin','abcd')
        response = self.app.get('/apiKey')
        self.assertEqual(response.status_code,200)
        key = response.get_json()
        response = self.app.get('/token_route', query_string=key)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data, b'Success')
        self.logout_user()



if __name__ == '__main__':
    unittest.main()
    #SQLalchemy tutorial https://stackoverflow.com/questions/14719507/unit-tests-for-query-in-sqlalchemy
    #Flask tutorial https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-vii-unit-testing-legacy
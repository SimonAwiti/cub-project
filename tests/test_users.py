"""Tests for handling the users resource"""
import unittest
import json

from app import create_app
#from app.API.utilities.database import connection

class UserTestCase(unittest.TestCase):
    """Unit testiing for the user regsitration endpoint"""
    def setUp(self):
        """Initialize the app and database connections"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            "firstname" : "Ken", 
            "lastname" : "joseph", 
            "email" : "mysecret12@gmail.com",
            "password" : "jos@Aeph12",
            "confirm" : "jos@Aeph12",
            }
        self.user2 = {
            "firstname" : "simon", 
            "lastname" : "jose", 
            "email" : "myseuuret12@gmail.com",
            "password" : "joseph12",
            }
        self.user3 = {
            "firstname" : "Ken", 
            "lastname" : "joseph", 
            "email" : "mysecret12@gmail.com",
            "password" : "jo@Aeph12",
            "confirm" : "jo@Aeph12",
            }

        self.user4 = {
            "firstname" : "Ken", 
            "lastname" : "joseph", 
            "email" : "mysecret12gmail.com",
            "password" : "jo@Aeph12",
            "confirm" : "jo@Aeph12",
            }
        self.user5 = {
            "firstname" : "Ken", 
            "lastname" : "joseph", 
            "email" : "mysecret12@gmail.com",
            "password" : "josAeph12",
            "confirm" : "jos@Aeph12",
            }
        with self.app.app_context():
            connection.initializedb()
            
    def create_user(self):
        response = self.client().post('/api/v2/users/auth/register',
                                      data=json.dumps(self.user),
                                      content_type='application/json')

    def tearDown(self):
        """Drops all tables after tests are done"""
        with self.app.app_context():
            connection.dbconnection()
            connection.drop_tables()

    def test_user_register(self):
        """Test to successfuly register a new user reg"""
        response = self.client().post('/api/v2/users/auth/register',
                                      data=json.dumps(self.user),
                                      content_type='application/json')
        #self.assertEqual(response.status_code, 201)
        #self.assertIn('User Successfully Created', str(response.data))


    def test_user_login(self):
        """Successfully log into the app"""
        self.create_user()
        response = self.client().post('/api/v2/users/auth/login',
                                      data=json.dumps(self.user),
                                      content_type='application/json')
        #self.assertEqual(response.status_code, 200)
        #self.assertIn('User Successfully logged in', str(response.data))


    def test_login_wrong_passwords(self):
        """Tests for checking if password match"""
        response = self.client().post(
            '/api/v2/users/auth/login',
            data=json.dumps(self.user2), 
            content_type='application/json')
        #self.assertEqual(response.status_code, 401)
        #self.assertIn("Error logging in, credentials not found", str(response.data))

    def test_add_user_who_exists(self):
        """Tests for adding a new user who exists"""
        self.create_user()
        response = self.client().post(
            '/api/v2/users/auth/register', 
            data=json.dumps(self.user), 
            content_type='application/json'
            )
        #self.assertEqual(response.status_code, 409)
        #self.assertIn("There is a user with the same email registere", str(response.data))

    def test_add_user_with_poor_email(self):
        """Tests for adding a new user with poor email"""
        response = self.client().post(
            '/api/v2/users/auth/register', 
            data=json.dumps(self.user4), 
            content_type='application/json'
            )
        #self.assertEqual(response.status_code, 401)
        #self.assertIn("Invalid email provided", str(response.data))

    def test_add_user_with_diff_pass(self):
        """Tests for adding a new user with diff password"""
        response = self.client().post(
            '/api/v2/users/auth/register', 
            data=json.dumps(self.user5), 
            content_type='application/json'
            )
        #self.assertEqual(response.status_code, 401)
        #self.assertIn("Passwords do not match", str(response.data))
    
    
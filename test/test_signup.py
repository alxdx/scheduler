import unittest
import json
from server import server as app
from database.db import db

class SignupTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()
    def test_successfull_signup(self):
        payload= json.dumps({
                    "matricula": "201750505",
                    "name": "pepe pollo",
                    "mail": "correo@mail.com",
                    "password": "jijiji"        	
                })
        response = self.app.post("api/auth/signup",headers={"Content-Type":"application/json"},data=payload)      
        
        #self.assertEqual(str,type(response.json['id']))
        self.assertEqual(200,response.status_code)
    def tearDown(self):
        self.db.drop_collection('alumno')

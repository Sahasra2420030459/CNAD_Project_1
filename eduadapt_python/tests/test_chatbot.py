import unittest
import json
from app import create_app
from models import db, User
from config import Config
from chatbot import generate_local_response

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Login student
        self.client.post('/register', data={
            'name': 'Chat Student',
            'email': 'chat@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_local_rule_greetings(self):
        reply = generate_local_response("Hello there!")
        self.assertIn("EduAdapt-AI Learning Tutor", reply)

    def test_local_rule_big_o(self):
        reply = generate_local_response("Can you explain Big-O notation?")
        self.assertIn("Big-O Notation", reply)
        self.assertIn("O(1)", reply)

    def test_local_rule_hint_mode(self):
        reply = generate_local_response("Give me a hint for question 3, don't give the answer")
        self.assertIn("EduAdapt Conceptual Hint", reply)
        self.assertIn("Core Invariant", reply)

    def test_api_chat_endpoint(self):
        res = self.client.post('/api/chat', 
                               data=json.dumps({'message': 'How do I unlock Level 2?'}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn('response', data)
        self.assertIn('70%', data['response'])
        self.assertEqual(data['source'], 'local_rule_tutor')
        self.assertIn('timestamp', data)

    def test_api_chat_empty_message_validation(self):
        res = self.client.post('/api/chat', 
                               data=json.dumps({'message': '   '}),
                               content_type='application/json')
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()

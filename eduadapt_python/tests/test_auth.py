import unittest
from app import create_app
from models import db, User
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_success(self):
        response = self.client.post('/register', data={
            'name': 'Test Student',
            'email': 'student@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to EduAdapt-AI', response.data)
        
        user = User.query.filter_by(email='student@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test Student')
        self.assertTrue(user.check_password('password123'))

    def test_register_duplicate_email(self):
        self.client.post('/register', data={
            'name': 'User One',
            'email': 'dup@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.client.get('/logout')
        response = self.client.post('/register', data={
            'name': 'User Two',
            'email': 'dup@example.com',
            'password': 'password456',
            'confirm_password': 'password456'
        }, follow_redirects=True)
        self.assertIn(b'already exists', response.data)

    def test_register_password_mismatch(self):
        response = self.client.post('/register', data={
            'name': 'User Mismatch',
            'email': 'mismatch@example.com',
            'password': 'password123',
            'confirm_password': 'different_password'
        }, follow_redirects=True)
        self.assertIn(b'Passwords do not match', response.data)

    def test_login_and_logout(self):
        # Register first
        self.client.post('/register', data={
            'name': 'Login Tester',
            'email': 'login@example.com',
            'password': 'secretpassword',
            'confirm_password': 'secretpassword'
        })
        # Log out
        self.client.get('/logout')

        # Attempt invalid login
        bad_login = self.client.post('/login', data={
            'email': 'login@example.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertIn(b'Invalid email or password', bad_login.data)

        # Valid login
        good_login = self.client.post('/login', data={
            'email': 'login@example.com',
            'password': 'secretpassword'
        }, follow_redirects=True)
        self.assertEqual(good_login.status_code, 200)
        self.assertIn(b'Welcome back, Login Tester', good_login.data)

        # Protected route accessible
        dash = self.client.get('/dashboard')
        self.assertEqual(dash.status_code, 200)
        self.assertIn(b'Login Tester', dash.data)

        # Log out
        logout_res = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'You have been safely signed out', logout_res.data)

    def test_protected_routes_redirect_unauthenticated(self):
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()

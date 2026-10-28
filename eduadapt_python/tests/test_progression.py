import unittest
from app import create_app
from models import db, User, StudentSubject, StudentProgress, AssignmentAttempt
from config import Config
from content import get_assignment_questions

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'

class ProgressionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Register and login a student
        self.client.post('/register', data={
            'name': 'Progression Student',
            'email': 'prog@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.user = User.query.filter_by(email='prog@example.com').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_initial_level_unlock_states(self):
        # Python should be auto-enrolled on registration
        can_access_easy, _ = self.user.can_access_level('python', 'easy')
        can_access_med, med_reason = self.user.can_access_level('python', 'medium')
        can_access_cmp, cmp_reason = self.user.can_access_level('python', 'complex')

        self.assertTrue(can_access_easy)
        self.assertFalse(can_access_med)
        self.assertIn("Level 2 (Medium) is locked", med_reason)
        self.assertFalse(can_access_cmp)
        self.assertIn("Level 3 (Complex) is locked", cmp_reason)

    def test_direct_url_access_blocked_for_locked_level(self):
        # Attempt to access /learn/python/medium directly via URL manipulation
        response = self.client.get('/learn/python/medium', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Level 2 (Medium) is locked', response.data)

        # Attempt to access /assignment/python/medium directly
        res_assign = self.client.get('/assignment/python/medium', follow_redirects=True)
        self.assertEqual(res_assign.status_code, 200)
        self.assertIn(b'Level 2 (Medium) is locked', res_assign.data)

    def test_pass_easy_unlocks_medium(self):
        questions = get_assignment_questions('python', 'easy')
        
        # Submit 10/10 correct answers (100%)
        form_data = {}
        for q in questions:
            form_data[f"q_{q['id']}"] = str(q['correct_index'])

        submit_res = self.client.post('/assignment/python/easy/submit', data=form_data, follow_redirects=True)
        self.assertEqual(submit_res.status_code, 200)
        self.assertIn(b'Assessment Passed!', submit_res.data)
        self.assertIn(b'100.0%', submit_res.data)

        # Verify database record updated
        prog = StudentProgress.query.filter_by(user_id=self.user.id, subject_id='python').first()
        self.assertTrue(prog.medium_unlocked)
        self.assertFalse(prog.complex_unlocked)

        # Now student can access medium learning page
        med_learn = self.client.get('/learn/python/medium')
        self.assertEqual(med_learn.status_code, 200)
        self.assertIn(b'Functions, Scope', med_learn.data)

    def test_fail_easy_keeps_medium_locked(self):
        questions = get_assignment_questions('python', 'easy')
        
        # Submit all wrong answers (0%)
        form_data = {}
        for q in questions:
            wrong_idx = (q['correct_index'] + 1) % 4
            form_data[f"q_{q['id']}"] = str(wrong_idx)

        submit_res = self.client.post('/assignment/python/easy/submit', data=form_data, follow_redirects=True)
        self.assertIn(b'Assessment Incomplete', submit_res.data)
        self.assertIn(b'0.0%', submit_res.data)

        # Verify Medium remains locked
        prog = StudentProgress.query.filter_by(user_id=self.user.id, subject_id='python').first()
        self.assertFalse(prog.medium_unlocked)

    def test_tenant_isolation_prevents_viewing_other_student_result(self):
        # Create an attempt for student 1
        attempt = AssignmentAttempt(
            user_id=self.user.id,
            subject_id='python',
            level='easy',
            score=8,
            total_questions=10,
            percentage=80.0,
            passed=True
        )
        db.session.add(attempt)
        db.session.commit()
        attempt_id = attempt.id

        # Switch to Student 2
        self.client.get('/logout')
        self.client.post('/register', data={
            'name': 'Student Two',
            'email': 'two@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })

        # Student 2 tries to view Student 1's attempt
        response = self.client.get(f'/assignment/result/{attempt_id}')
        # Should return 403 Forbidden
        self.assertEqual(response.status_code, 403)

if __name__ == '__main__':
    unittest.main()

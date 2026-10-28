import unittest
from content import ASSIGNMENT_QUESTIONS, get_assignment_questions

class AssignmentsTestCase(unittest.TestCase):
    def test_curriculum_questions_integrity(self):
        subjects = ['python', 'java', 'dbms', 'dsa']
        levels = ['easy', 'medium', 'complex']

        total_questions = 0
        for subj in subjects:
            self.assertIn(subj, ASSIGNMENT_QUESTIONS)
            for lvl in levels:
                questions = get_assignment_questions(subj, lvl)
                # Requirement: At least 10 questions per subject per level
                self.assertGreaterEqual(len(questions), 10, f"Subject {subj} Level {lvl} must have at least 10 questions")
                total_questions += len(questions)

                for q in questions:
                    self.assertIn('id', q)
                    self.assertIn('question', q)
                    self.assertIn('options', q)
                    self.assertEqual(len(q['options']), 4, f"Question {q['id']} must have exactly 4 options")
                    self.assertIn('correct_index', q)
                    self.assertIn(q['correct_index'], [0, 1, 2, 3], f"Question {q['id']} correct_index must be 0-3")
                    self.assertIn('explanation', q)
                    self.assertGreater(len(q['explanation']), 10, f"Question {q['id']} must have a substantive explanation")

        # 4 subjects * 3 levels * 10 questions = at least 120 questions
        self.assertGreaterEqual(total_questions, 120)

if __name__ == '__main__':
    unittest.main()

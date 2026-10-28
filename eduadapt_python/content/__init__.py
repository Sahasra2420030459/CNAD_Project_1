"""
Educational content and curriculum for EduAdapt-AI.
Covers 4 Subjects:
1. Python Programming
2. Java Programming
3. Database Management Systems (DBMS)
4. Data Structures and Algorithms (DSA)

Each subject contains 3 distinct levels:
- Easy (Level 1): Foundational, beginner-friendly, syntax, step-by-step
- Medium (Level 2): Intermediate, problem solving, practical application
- Complex (Level 3): Advanced, optimization, enterprise architectures, interview prep
"""

from .python_content import PYTHON_DATA
from .java_content import JAVA_DATA
from .dbms_content import DBMS_DATA
from .dsa_content import DSA_DATA
from .questions import ASSIGNMENT_QUESTIONS

SUBJECTS_CATALOG = {
    'python': PYTHON_DATA,
    'java': JAVA_DATA,
    'dbms': DBMS_DATA,
    'dsa': DSA_DATA
}

def get_subject_data(subject_id):
    return SUBJECTS_CATALOG.get(subject_id)

def get_level_data(subject_id, level):
    subj = get_subject_data(subject_id)
    if not subj:
        return None
    return subj.get('levels', {}).get(level.lower())

def get_topic_data(subject_id, level, topic_id):
    level_data = get_level_data(subject_id, level)
    if not level_data:
        return None
    for topic in level_data.get('topics', []):
        if topic['id'] == topic_id:
            return topic
    return None

def get_assignment_questions(subject_id, level):
    subj_questions = ASSIGNMENT_QUESTIONS.get(subject_id, {})
    return subj_questions.get(level.lower(), [])

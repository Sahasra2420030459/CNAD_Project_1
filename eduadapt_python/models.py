from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    enrolled_subjects = db.relationship('StudentSubject', backref='student', lazy=True, cascade='all, delete-orphan')
    progress = db.relationship('StudentProgress', backref='student', lazy=True, cascade='all, delete-orphan')
    assignment_attempts = db.relationship('AssignmentAttempt', backref='student', lazy=True, cascade='all, delete-orphan')
    topic_completions = db.relationship('TopicProgress', backref='student', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='student', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_enrolled_in(self, subject_id):
        return StudentSubject.query.filter_by(user_id=self.id, subject_id=subject_id).first() is not None

    def get_progress(self, subject_id):
        return StudentProgress.query.filter_by(user_id=self.id, subject_id=subject_id).first()

    def can_access_level(self, subject_id, level):
        """
        Server-side validation for level access:
        - 'easy': unlocked if student is enrolled in subject
        - 'medium': unlocked only if easy level assignment is passed (>= 70%)
        - 'complex': unlocked only if medium level assignment is passed (>= 70%)
        """
        if not self.is_enrolled_in(subject_id):
            return False, "You are not enrolled in this subject. Please enroll from the Subjects page."
        
        progress = self.get_progress(subject_id)
        if not progress:
            return False, "Progress record not found for this subject."
        
        lvl = level.lower().strip()
        if lvl == 'easy':
            return True, "Unlocked"
        elif lvl == 'medium':
            if progress.medium_unlocked:
                return True, "Unlocked"
            return False, "Level 2 (Medium) is locked! You must first pass the Level 1 (Easy) assignment with at least 70%."
        elif lvl == 'complex':
            if progress.complex_unlocked:
                return True, "Unlocked"
            return False, "Level 3 (Complex) is locked! You must first pass the Level 2 (Medium) assignment with at least 70%."
        return False, f"Invalid level: {level}"


class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.String(50), primary_key=True)  # 'python', 'java', 'dbms', 'dsa'
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    short_summary = db.Column(db.String(255), nullable=False)
    icon = db.Column(db.String(50), default='bi-journal-code')
    badge_color = db.Column(db.String(30), default='primary')
    difficulty = db.Column(db.String(50), default='Beginner to Advanced')
    topics_count = db.Column(db.Integer, default=27)  # approx ~9 topics * 3 levels


class StudentSubject(db.Model):
    __tablename__ = 'student_subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.String(50), db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'subject_id', name='uq_student_subject'),
    )


class StudentProgress(db.Model):
    __tablename__ = 'student_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.String(50), db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    current_level = db.Column(db.String(20), default='easy')  # 'easy', 'medium', 'complex'
    easy_unlocked = db.Column(db.Boolean, default=True)
    medium_unlocked = db.Column(db.Boolean, default=False)
    complex_unlocked = db.Column(db.Boolean, default=False)
    is_completed = db.Column(db.Boolean, default=False)
    last_studied_topic_id = db.Column(db.String(100), nullable=True)
    last_studied_topic_title = db.Column(db.String(200), nullable=True)
    last_studied_level = db.Column(db.String(20), nullable=True)
    last_studied_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'subject_id', name='uq_student_subject_progress'),
    )


class TopicProgress(db.Model):
    __tablename__ = 'topic_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    topic_id = db.Column(db.String(100), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'subject_id', 'level', 'topic_id', name='uq_user_topic'),
    )


class AssignmentAttempt(db.Model):
    __tablename__ = 'assignment_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    subject_id = db.Column(db.String(50), db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)
    answers_json = db.Column(db.Text, nullable=True)  # JSON string of submitted vs correct
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    subject_context = db.Column(db.String(50), nullable=True)
    level_context = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

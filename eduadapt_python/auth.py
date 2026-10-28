import re
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from models import db, User, Subject, StudentSubject, StudentProgress
from content import SUBJECTS_CATALOG

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('learning.dashboard'))
        
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Server-side validations
        if not name or len(name) < 2:
            flash("Please provide your full name (at least 2 characters).", "danger")
            return render_template('auth/register.html', name=name, email=email)

        # Email regex format validation
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            flash("Please provide a valid email address.", "danger")
            return render_template('auth/register.html', name=name, email=email)

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template('auth/register.html', name=name, email=email)

        if password != confirm_password:
            flash("Passwords do not match. Please re-enter.", "danger")
            return render_template('auth/register.html', name=name, email=email)

        # Check existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("An account with this email address already exists. Please log in.", "warning")
            return redirect(url_for('auth.login'))

        # Create new user
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.flush()  # Get user.id

            # Auto-enroll in default foundational subjects (e.g., Python & DBMS) to provide immediate value
            for subj_id in ['python', 'dbms']:
                student_sub = StudentSubject(user_id=new_user.id, subject_id=subj_id)
                db.session.add(student_sub)
                
                # Initialize progression
                prog = StudentProgress(
                    user_id=new_user.id,
                    subject_id=subj_id,
                    current_level='easy',
                    easy_unlocked=True,
                    medium_unlocked=False,
                    complex_unlocked=False,
                    is_completed=False
                )
                db.session.add(prog)

            db.session.commit()
            
            # Log in automatically
            session.clear()
            session['user_id'] = new_user.id
            session['user_name'] = new_user.name
            session.permanent = True
            
            flash(f"Welcome to EduAdapt-AI, {new_user.name}! Your account has been created successfully.", "success")
            return redirect(url_for('learning.dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred during registration. Please try again.", "danger")
            return render_template('auth/register.html', name=name, email=email)

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('learning.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        if not email or not password:
            flash("Please enter both email and password.", "danger")
            return render_template('auth/login.html', email=email)

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password. Please check your credentials.", "danger")
            return render_template('auth/login.html', email=email)

        # Successful login
        session.clear()
        session['user_id'] = user.id
        session['user_name'] = user.name
        session.permanent = remember

        flash(f"Welcome back, {user.name}!", "success")
        
        next_url = request.args.get('next')
        if next_url and next_url.startswith('/'):
            return redirect(next_url)
        return redirect(url_for('learning.dashboard'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    user_name = session.get('user_name', 'Student')
    session.clear()
    flash(f"You have been safely signed out. See you soon, {user_name}!", "info")
    return redirect(url_for('auth.login'))

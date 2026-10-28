import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, abort
from models import db, User, StudentProgress, AssignmentAttempt
from auth import login_required
from content import SUBJECTS_CATALOG, get_subject_data, get_level_data, get_assignment_questions

assignments_bp = Blueprint('assignments', __name__)

PASSING_PERCENTAGE = 70.0

@assignments_bp.route('/assignments')
@login_required
def index():
    user = g.user
    enrolled_subs = user.enrolled_subjects
    enrolled_ids = {e.subject_id for e in enrolled_subs}
    
    # Gather assessments info across enrolled subjects
    assessments_summary = []
    for subj_id in enrolled_ids:
        subj = get_subject_data(subj_id)
        if not subj:
            continue
            
        prog = user.get_progress(subj_id)
        
        for lvl in ['easy', 'medium', 'complex']:
            lvl_meta = get_level_data(subj_id, lvl)
            can_take, lock_msg = user.can_access_level(subj_id, lvl)
            
            # Find best attempt
            best_attempt = AssignmentAttempt.query.filter_by(
                user_id=user.id,
                subject_id=subj_id,
                level=lvl
            ).order_by(AssignmentAttempt.score.desc()).first()
            
            # Find total attempts
            attempts_count = AssignmentAttempt.query.filter_by(
                user_id=user.id,
                subject_id=subj_id,
                level=lvl
            ).count()
            
            lvl_title = "Level 1: Easy" if lvl == 'easy' else "Level 2: Medium" if lvl == 'medium' else "Level 3: Complex"
            
            assessments_summary.append({
                'subject_id': subj_id,
                'subject_title': subj['title'],
                'badge_color': subj.get('badge_color', 'primary'),
                'icon': subj.get('icon', 'bi-journal-code'),
                'level': lvl,
                'level_title': lvl_title,
                'can_take': can_take,
                'lock_msg': lock_msg,
                'best_attempt': best_attempt,
                'attempts_count': attempts_count,
                'is_passed': best_attempt.passed if best_attempt else False
            })
            
    return render_template(
        'assignments/index.html',
        assessments_summary=assessments_summary,
        total_enrolled=len(enrolled_ids)
    )

@assignments_bp.route('/assignment/<subject_id>/<level>', methods=['GET'])
@login_required
def take_assignment(subject_id, level):
    user = g.user
    lvl = level.lower().strip()
    
    subj = get_subject_data(subject_id)
    if not subj:
        flash(f"Subject '{subject_id}' not found.", "danger")
        return redirect(url_for('assignments.index'))
        
    # Strict server-side verification: Can this student access this level's assessment?
    can_access, reason = user.can_access_level(subject_id, lvl)
    if not can_access:
        flash(reason, "danger")
        return redirect(url_for('learning.learn_subject_overview', subject_id=subject_id))
        
    questions = get_assignment_questions(subject_id, lvl)
    if not questions or len(questions) == 0:
        flash("Assessment questions are being generated for this level. Please check back shortly.", "warning")
        return redirect(url_for('learning.learn_subject_overview', subject_id=subject_id))
        
    # Get previous attempts count
    prior_attempts = AssignmentAttempt.query.filter_by(
        user_id=user.id,
        subject_id=subject_id,
        level=lvl
    ).count()
    
    lvl_title = "Level 1: Easy (Foundations)" if lvl == 'easy' else "Level 2: Medium (Problem Solving)" if lvl == 'medium' else "Level 3: Complex (Advanced)"
    
    return render_template(
        'assignments/assessment.html',
        subject=subj,
        level=lvl,
        level_title=lvl_title,
        questions=questions,
        total_questions=len(questions),
        prior_attempts=prior_attempts,
        passing_percentage=PASSING_PERCENTAGE
    )

@assignments_bp.route('/assignment/<subject_id>/<level>/submit', methods=['POST'])
@login_required
def submit_assignment(subject_id, level):
    user = g.user
    lvl = level.lower().strip()
    
    subj = get_subject_data(subject_id)
    if not subj:
        flash(f"Subject '{subject_id}' not found.", "danger")
        return redirect(url_for('assignments.index'))
        
    # Strict server-side verification
    can_access, reason = user.can_access_level(subject_id, lvl)
    if not can_access:
        flash(reason, "danger")
        return redirect(url_for('learning.learn_subject_overview', subject_id=subject_id))
        
    questions = get_assignment_questions(subject_id, lvl)
    if not questions:
        flash("No questions found for this assessment.", "danger")
        return redirect(url_for('assignments.index'))
        
    # SERVER-SIDE SCORING
    correct_count = 0
    total_count = len(questions)
    detailed_answers = []
    
    for idx, q in enumerate(questions):
        form_field = f"q_{q['id']}"
        raw_choice = request.form.get(form_field)
        
        student_choice = None
        if raw_choice is not None and raw_choice.isdigit():
            student_choice = int(raw_choice)
            
        is_correct = (student_choice == q['correct_index'])
        if is_correct:
            correct_count += 1
            
        student_answer_text = q['options'][student_choice] if (student_choice is not None and 0 <= student_choice < len(q['options'])) else "No answer provided"
        correct_answer_text = q['options'][q['correct_index']]
        
        detailed_answers.append({
            'question_id': q['id'],
            'question_text': q['question'],
            'options': q['options'],
            'student_choice': student_choice,
            'student_answer_text': student_answer_text,
            'correct_index': q['correct_index'],
            'correct_answer_text': correct_answer_text,
            'is_correct': is_correct,
            'explanation': q['explanation']
        })
        
    percentage = round((correct_count / total_count) * 100.0, 1) if total_count > 0 else 0.0
    passed = percentage >= PASSING_PERCENTAGE
    
    # Save attempt in database
    attempt = AssignmentAttempt(
        user_id=user.id,
        subject_id=subject_id,
        level=lvl,
        score=correct_count,
        total_questions=total_count,
        percentage=percentage,
        passed=passed,
        answers_json=json.dumps(detailed_answers),
        completed_at=datetime.utcnow()
    )
    db.session.add(attempt)
    
    # SERVER-SIDE LEVEL PROGRESSION UNLOCKING
    prog = user.get_progress(subject_id)
    unlock_message = None
    
    if prog and passed:
        if lvl == 'easy':
            if not prog.medium_unlocked:
                prog.medium_unlocked = True
                unlock_message = "Level 2 (Medium) has been unlocked!"
            if prog.current_level == 'easy':
                prog.current_level = 'medium'
                
        elif lvl == 'medium':
            if not prog.complex_unlocked:
                prog.complex_unlocked = True
                unlock_message = "Level 3 (Complex) has been unlocked!"
            if prog.current_level == 'medium':
                prog.current_level = 'complex'
                
        elif lvl == 'complex':
            if not prog.is_completed:
                prog.is_completed = True
                unlock_message = "Mastery Achieved! You have successfully completed the entire learning path for this subject!"
                
    db.session.commit()
    
    if passed:
        congrats = f"Congratulations! You scored {percentage}% ({correct_count}/{total_count}) and PASSED!"
        if unlock_message:
            congrats += f" 🚀 {unlock_message}"
        flash(congrats, "success")
    else:
        flash(f"You scored {percentage}% ({correct_count}/{total_count}). A score of {PASSING_PERCENTAGE}% is required to pass. Please review the learning material and try again!", "warning")
        
    return redirect(url_for('assignments.view_result', attempt_id=attempt.id))

@assignments_bp.route('/assignment/result/<int:attempt_id>')
@login_required
def view_result(attempt_id):
    user = g.user
    attempt = AssignmentAttempt.query.get_or_404(attempt_id)
    
    # Strict tenant / student isolation: prevent students from viewing others' results
    if attempt.user_id != user.id:
        flash("You do not have permission to view another student's assignment results.", "danger")
        abort(403)
        
    subj = get_subject_data(attempt.subject_id)
    detailed_answers = json.loads(attempt.answers_json) if attempt.answers_json else []
    prog = user.get_progress(attempt.subject_id)
    
    # Next level information
    next_level = None
    if attempt.level == 'easy' and prog and prog.medium_unlocked:
        next_level = 'medium'
    elif attempt.level == 'medium' and prog and prog.complex_unlocked:
        next_level = 'complex'
        
    return render_template(
        'assignments/result.html',
        attempt=attempt,
        subject=subj,
        detailed_answers=detailed_answers,
        progress=prog,
        next_level=next_level,
        passing_percentage=PASSING_PERCENTAGE
    )

@assignments_bp.route('/assignment/history')
@login_required
def history():
    user = g.user
    attempts = AssignmentAttempt.query.filter_by(user_id=user.id).order_by(AssignmentAttempt.completed_at.desc()).all()
    
    history_items = []
    for a in attempts:
        subj = get_subject_data(a.subject_id)
        history_items.append({
            'attempt': a,
            'subject_title': subj['title'] if subj else a.subject_id,
            'badge_color': subj.get('badge_color', 'primary') if subj else 'secondary'
        })
        
    return render_template('assignments/history.html', history_items=history_items)

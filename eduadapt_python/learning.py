from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g, jsonify
from models import db, User, Subject, StudentSubject, StudentProgress, TopicProgress, AssignmentAttempt
from auth import login_required
from content import SUBJECTS_CATALOG, get_subject_data, get_level_data, get_topic_data

learning_bp = Blueprint('learning', __name__)

@learning_bp.route('/')
def home():
    if g.user:
        return redirect(url_for('learning.dashboard'))
    return render_template('index.html', catalog=SUBJECTS_CATALOG)

@learning_bp.route('/dashboard')
@login_required
def dashboard():
    user = g.user
    
    # Enrolled subjects
    enrollments = StudentSubject.query.filter_by(user_id=user.id).all()
    enrolled_subject_ids = [e.subject_id for e in enrollments]
    
    # Progress records
    progress_records = StudentProgress.query.filter_by(user_id=user.id).all()
    progress_map = {p.subject_id: p for p in progress_records}
    
    # Enrolled subjects details list
    enrolled_details = []
    for subj_id in enrolled_subject_ids:
        subj_meta = get_subject_data(subj_id)
        if not subj_meta:
            continue
        
        prog = progress_map.get(subj_id)
        
        # Calculate level completion ratio
        levels_passed = 0
        if prog:
            if prog.medium_unlocked:
                levels_passed += 1
            if prog.complex_unlocked:
                levels_passed += 1
            if prog.is_completed:
                levels_passed += 1
                
        progress_pct = int((levels_passed / 3) * 100)
        
        # Determine highest unlocked level badge
        current_tier = 'Easy'
        if prog:
            if prog.is_completed:
                current_tier = 'Completed (All 3 Levels)'
            elif prog.complex_unlocked:
                current_tier = 'Complex (Level 3)'
            elif prog.medium_unlocked:
                current_tier = 'Medium (Level 2)'
            else:
                current_tier = 'Easy (Level 1)'
                
        enrolled_details.append({
            'id': subj_id,
            'title': subj_meta['title'],
            'icon': subj_meta.get('icon', 'bi-journal-code'),
            'badge_color': subj_meta.get('badge_color', 'primary'),
            'current_tier': current_tier,
            'prog': prog,
            'progress_pct': progress_pct,
            'is_completed': prog.is_completed if prog else False
        })
    
    # Assignment statistics
    attempts = AssignmentAttempt.query.filter_by(user_id=user.id).order_by(AssignmentAttempt.completed_at.desc()).all()
    total_assignments_completed = len(attempts)
    passed_assignments_count = sum(1 for a in attempts if a.passed)
    average_score = round(sum(a.percentage for a in attempts) / total_assignments_completed, 1) if total_assignments_completed > 0 else 0.0
    
    # Overall learning progress
    total_subjects_count = len(SUBJECTS_CATALOG)
    completed_subjects_count = sum(1 for p in progress_records if p.is_completed)
    overall_progress_pct = int((completed_subjects_count / total_subjects_count) * 100) if total_subjects_count > 0 else 0
    
    # Recent attempts (last 5)
    recent_attempts = attempts[:5]
    
    # Recently studied subjects
    recent_progress = [p for p in progress_records if p.last_studied_topic_title]
    recent_progress.sort(key=lambda x: x.last_studied_at or datetime.min, reverse=True)
    
    return render_template(
        'dashboard.html',
        user=user,
        enrolled_details=enrolled_details,
        all_catalog=SUBJECTS_CATALOG,
        total_enrolled=len(enrolled_subject_ids),
        completed_subjects_count=completed_subjects_count,
        total_assignments_completed=total_assignments_completed,
        passed_assignments_count=passed_assignments_count,
        average_score=average_score,
        overall_progress_pct=overall_progress_pct,
        recent_attempts=recent_attempts,
        recent_progress=recent_progress
    )

@learning_bp.route('/subjects')
@login_required
def subjects():
    user = g.user
    enrolled_ids = {e.subject_id for e in StudentSubject.query.filter_by(user_id=user.id).all()}
    
    # Prepare subjects with enrollment status
    subjects_list = []
    for subj_id, data in SUBJECTS_CATALOG.items():
        is_enrolled = subj_id in enrolled_ids
        prog = StudentProgress.query.filter_by(user_id=user.id, subject_id=subj_id).first() if is_enrolled else None
        
        subjects_list.append({
            'id': subj_id,
            'title': data['title'],
            'description': data['description'],
            'short_summary': data['short_summary'],
            'icon': data.get('icon', 'bi-journal-code'),
            'badge_color': data.get('badge_color', 'primary'),
            'difficulty': data.get('difficulty', 'Beginner to Advanced'),
            'is_enrolled': is_enrolled,
            'progress': prog
        })
        
    return render_template('subjects.html', subjects=subjects_list)

@learning_bp.route('/subjects/enroll', methods=['POST'])
@login_required
def enroll_subject():
    user = g.user
    subject_ids = request.form.getlist('subject_ids')
    single_subject = request.form.get('subject_id')
    
    if single_subject and single_subject not in subject_ids:
        subject_ids.append(single_subject)
        
    if not subject_ids:
        flash("Please select at least one subject to enroll.", "warning")
        return redirect(url_for('learning.subjects'))
        
    enrolled_count = 0
    for subj_id in subject_ids:
        if subj_id in SUBJECTS_CATALOG:
            # Check if already enrolled
            existing = StudentSubject.query.filter_by(user_id=user.id, subject_id=subj_id).first()
            if not existing:
                enrollment = StudentSubject(user_id=user.id, subject_id=subj_id)
                db.session.add(enrollment)
                
                # Create initial progress
                prog = StudentProgress(
                    user_id=user.id,
                    subject_id=subj_id,
                    current_level='easy',
                    easy_unlocked=True,
                    medium_unlocked=False,
                    complex_unlocked=False,
                    is_completed=False
                )
                db.session.add(prog)
                enrolled_count += 1
                
    db.session.commit()
    if enrolled_count > 0:
        flash(f"Successfully enrolled in {enrolled_count} subject(s)! You can begin learning Level 1 (Easy).", "success")
    else:
        flash("You are already enrolled in the selected subject(s).", "info")
        
    return redirect(url_for('learning.dashboard'))

@learning_bp.route('/subjects/unenroll', methods=['POST'])
@login_required
def unenroll_subject():
    user = g.user
    subject_id = request.form.get('subject_id')
    
    if not subject_id:
        flash("Subject ID is required.", "danger")
        return redirect(url_for('learning.subjects'))
        
    enrollment = StudentSubject.query.filter_by(user_id=user.id, subject_id=subject_id).first()
    if enrollment:
        db.session.delete(enrollment)
        
        # Also clean up progress
        prog = StudentProgress.query.filter_by(user_id=user.id, subject_id=subject_id).first()
        if prog:
            db.session.delete(prog)
            
        db.session.commit()
        subj_meta = get_subject_data(subject_id)
        title = subj_meta['title'] if subj_meta else subject_id
        flash(f"You have unenrolled from {title}.", "info")
    else:
        flash("You are not currently enrolled in that subject.", "warning")
        
    return redirect(url_for('learning.subjects'))

@learning_bp.route('/learn/<subject_id>')
@login_required
def learn_subject_overview(subject_id):
    user = g.user
    subj_data = get_subject_data(subject_id)
    if not subj_data:
        flash(f"Subject '{subject_id}' was not found in our catalog.", "danger")
        return redirect(url_for('learning.subjects'))
        
    if not user.is_enrolled_in(subject_id):
        flash(f"You must enroll in {subj_data['title']} before accessing the curriculum.", "warning")
        return redirect(url_for('learning.subjects'))
        
    prog = user.get_progress(subject_id)
    
    # Gather level unlock states and quiz attempts
    levels_info = []
    level_keys = [('easy', 'Level 1: Easy (Foundations)'), 
                  ('medium', 'Level 2: Medium (Problem Solving)'), 
                  ('complex', 'Level 3: Complex (Advanced & Architecture)')]
                  
    for lvl_key, lvl_title in level_keys:
        lvl_data = subj_data['levels'].get(lvl_key)
        unlocked, lock_reason = user.can_access_level(subject_id, lvl_key)
        
        # Best attempt for this level
        best_attempt = AssignmentAttempt.query.filter_by(
            user_id=user.id,
            subject_id=subject_id,
            level=lvl_key
        ).order_by(AssignmentAttempt.score.desc()).first()
        
        levels_info.append({
            'key': lvl_key,
            'title': lvl_title,
            'data': lvl_data,
            'unlocked': unlocked,
            'lock_reason': lock_reason,
            'best_attempt': best_attempt,
            'topics_count': len(lvl_data.get('topics', [])) if lvl_data else 0
        })
        
    return render_template(
        'learning/subject_overview.html',
        subject=subj_data,
        progress=prog,
        levels_info=levels_info
    )

@learning_bp.route('/learn/<subject_id>/<level>')
@learning_bp.route('/learn/<subject_id>/<level>/<topic_id>')
@login_required
def learn_level(subject_id, level, topic_id=None):
    user = g.user
    lvl = level.lower().strip()
    
    subj_data = get_subject_data(subject_id)
    if not subj_data:
        flash(f"Subject '{subject_id}' not found.", "danger")
        return redirect(url_for('learning.subjects'))
        
    # Strict server-side access control
    can_access, reason = user.can_access_level(subject_id, lvl)
    if not can_access:
        flash(reason, "danger")
        return redirect(url_for('learning.learn_subject_overview', subject_id=subject_id))
        
    lvl_data = get_level_data(subject_id, lvl)
    if not lvl_data:
        flash(f"Level '{level}' not found for {subj_data['title']}.", "danger")
        return redirect(url_for('learning.learn_subject_overview', subject_id=subject_id))
        
    topics = lvl_data.get('topics', [])
    if not topics:
        flash("No topics available in this module yet.", "warning")
        return redirect(url_for('learning.learn_subject_overview', subject_id=subject_id))
        
    # Select active topic
    active_topic = None
    if topic_id:
        for t in topics:
            if t['id'] == topic_id:
                active_topic = t
                break
    if not active_topic:
        active_topic = topics[0]
        
    # Update student progress tracking
    prog = user.get_progress(subject_id)
    if prog:
        prog.last_studied_level = lvl
        prog.last_studied_topic_id = active_topic['id']
        prog.last_studied_topic_title = active_topic['title']
        prog.last_studied_at = datetime.utcnow()
        db.session.commit()
        
    # Completed topics list
    completed_topics = TopicProgress.query.filter_by(
        user_id=user.id,
        subject_id=subject_id,
        level=lvl
    ).all()
    completed_topic_ids = {ct.topic_id for ct in completed_topics}
    
    # Calculate previous and next topics for smooth navigation
    curr_idx = 0
    for idx, t in enumerate(topics):
        if t['id'] == active_topic['id']:
            curr_idx = idx
            break
            
    prev_topic = topics[curr_idx - 1] if curr_idx > 0 else None
    next_topic = topics[curr_idx + 1] if curr_idx < len(topics) - 1 else None
    
    return render_template(
        'learning/level_view.html',
        subject=subj_data,
        level=lvl,
        level_data=lvl_data,
        topics=topics,
        active_topic=active_topic,
        completed_topic_ids=completed_topic_ids,
        prev_topic=prev_topic,
        next_topic=next_topic,
        curr_idx=curr_idx + 1,
        total_topics=len(topics)
    )

@learning_bp.route('/api/topic/complete', methods=['POST'])
@login_required
def api_complete_topic():
    data = request.get_json() or {}
    subject_id = data.get('subject_id')
    level = data.get('level', '').lower()
    topic_id = data.get('topic_id')
    
    if not subject_id or not level or not topic_id:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
    user = g.user
    existing = TopicProgress.query.filter_by(
        user_id=user.id,
        subject_id=subject_id,
        level=level,
        topic_id=topic_id
    ).first()
    
    if not existing:
        tp = TopicProgress(
            user_id=user.id,
            subject_id=subject_id,
            level=level,
            topic_id=topic_id
        )
        db.session.add(tp)
        db.session.commit()
        
    total_completed = TopicProgress.query.filter_by(
        user_id=user.id,
        subject_id=subject_id,
        level=level
    ).count()
    
    return jsonify({
        'success': True,
        'message': 'Topic marked as completed',
        'completed_count': total_completed
    })

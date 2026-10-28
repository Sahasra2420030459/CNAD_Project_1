import os
from flask import Flask, render_template
from config import Config
from models import db, Subject
from content import SUBJECTS_CATALOG
from auth import auth_bp
from learning import learning_bp
from assignments import assignments_bp
from chatbot import chatbot_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(assignments_bp)
    app.register_blueprint(chatbot_bp)

    # Context processors
    @app.context_processor
    def inject_global_data():
        return {
            'app_name': 'EduAdapt-AI',
            'catalog': SUBJECTS_CATALOG,
            'current_year': 2026
        }

    # Custom Error Handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    # Safe Database Schema Initialization
    with app.app_context():
        db.create_all()
        # Seed or sync subject records in db
        try:
            for s_id, s_data in SUBJECTS_CATALOG.items():
                existing = Subject.query.get(s_id)
                if not existing:
                    new_subj = Subject(
                        id=s_id,
                        title=s_data['title'],
                        description=s_data['description'],
                        short_summary=s_data.get('short_summary', ''),
                        icon=s_data.get('icon', 'bi-journal-code'),
                        badge_color=s_data.get('badge_color', 'primary'),
                        difficulty=s_data.get('difficulty', 'Beginner to Advanced'),
                        topics_count=27
                    )
                    db.session.add(new_subj)
            db.session.commit()
        except Exception:
            db.session.rollback()

    return app

app = create_app()

if __name__ == '__main__':
    # Determine port from environment (e.g. Render sets PORT)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 't')
    print(f"Starting EduAdapt-AI Platform on http://127.0.0.1:{port} (Debug={debug_mode})")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)

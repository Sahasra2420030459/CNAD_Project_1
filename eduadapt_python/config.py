import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'eduadapt-ai-super-secret-dev-key-' + secrets.token_hex(16)
    
    # Handle Database URL (Render / PostgreSQL compatibility)
    db_url = os.environ.get('DATABASE_URL')
    if db_url and db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = db_url or f"sqlite:///{os.path.join(basedir, 'eduadapt.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    
    # Optional AI integration keys
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or os.environ.get('AI_API_KEY')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

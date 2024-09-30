from starlette.middleware.sessions import SessionMiddleware
import os

class SessionConfig:
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'sessions')
    SESSION_FILE_THRESHOLD = 500
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'
    SESSION_USE_SIGNER = True
    SECRET_KEY = os.getenv('SECRET_KEY')

def init_session(app):
    app.add_middleware(SessionMiddleware, secret_key=SessionConfig.SECRET_KEY)

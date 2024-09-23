import os

class SessionConfig:
    # 세션 설정
    SESSION_TYPE = 'filesystem'  # 파일 시스템에 세션 저장
    SESSION_PERMANENT = False  # 세션 만료 시간을 명시적으로 설정
    PERMANENT_SESSION_LIFETIME = 3600  # 1시간 (초 단위)
    SESSION_FILE_DIR = os.path.join(os.getcwd(), 'sessions')  # 세션 파일 저장 경로
    SESSION_FILE_THRESHOLD = 500  # 최대 저장 가능한 세션 파일 수
    SESSION_COOKIE_HTTPONLY = True  # 자바스크립트에서 세션 쿠키 접근 불가
    
    # 환경에 따라 SESSION_COOKIE_SECURE 설정
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV') == 'production'  # production 환경에서는 True
    
    SESSION_USE_SIGNER = True  # 쿠키에 서명하여 변조 방지
    SECRET_KEY = os.getenv('SECRET_KEY')  # 비밀 키는 환경 변수에서 가져옴
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_session import Session
from config.session import SessionConfig
from flask_wtf.csrf import CSRFProtect

# 다른 모듈에서 블루프린트 가져오기
from routes.user_route import user_bp
from routes.csrf_route import csrf_bp

load_dotenv()

app = Flask(__name__)

# 환경변수에서 CORS 허용 출처 가져오기
CORS_ORIGIN = os.getenv('CORS_ORIGIN', '*')

# CORS 설정
CORS(app, resources={r'/*': {"origins": CORS_ORIGIN}})
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 세션 설정
app.config.from_object(SessionConfig)
Session(app)

# csrf 설정
CSRFProtect(app)

# 블루프린트 등록
app.register_blueprint(user_bp)
app.register_blueprint(csrf_bp)

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'error': 'Page not found'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)
    
# if __name__ == '__main__':
#     app.run(ssl_context='adhoc')  # 개발용 SSL : https
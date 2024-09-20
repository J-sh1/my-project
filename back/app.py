from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 다른 모듈에서 블루프린트 가져오기
from routes.user import user_bp

load_dotenv()

app = Flask(__name__)
# 환경변수에서 CORS 허용 출처 가져오기
CORS_ORIGIN = os.getenv('CORS_ORIGIN', '*')

# CORS 설정 - 환경변수에서 가져온 출처만 허용
CORS(app, resources={r'/*': {"origins": CORS_ORIGIN}})
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# 블루프린트 등록
app.register_blueprint(user_bp)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)
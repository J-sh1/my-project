from flask import jsonify, make_response
from flask_wtf.csrf import generate_csrf

def csrf_tokebn_res():
    csrf_token = generate_csrf()
    res = make_response(jsonify({"message": "CSRF token sent"}))  # 응답 본문에 CSRF 토큰 포함하지 않음
    res.set_cookie('csrf_token', csrf_token)  # CSRF 토큰을 쿠키에만 저장
    return res

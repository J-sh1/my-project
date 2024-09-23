from flask import jsonify, make_response
from flask_wtf.csrf import generate_csrf

def csrf_tokebn_res():
    res = make_response(jsonify({"message" : 'CSRF token'}))
    res.set_cookie('csrf_token', generate_csrf())
    return res
from config.db import db_con
from flask import Blueprint, request, jsonify

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods = ['POST'])
def login():
    
    return
from flask import Blueprint, jsonify, request
from ..models import Login
from .. import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    user = Login.query.filter_by(username=username).first()
    if user and user.password == password:
        return jsonify({
            "message": "Login successful",
            "username": user.username
        }), 200
    
    else:
        return jsonify({"message": "Invalid username or password"}), 401
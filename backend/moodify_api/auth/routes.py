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
    
@auth.route('/sign-up', methods=['POST'])
def signup():
    data = request.get_json();
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400
        # I don't think this will ever happen since I put required on the forms but just in case
    
    existing_user = Login.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409
    
    new_user = Login(
        username = username,
        password = password
    )

    try:
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"}), 201
    except Exception:
        db.session.rollback()
        print(f"Database error during signup: {Exception}")
        return jsonify({"message": "An internal error occured."}), 500
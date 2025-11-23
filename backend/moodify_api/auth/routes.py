from flask import Blueprint, jsonify, request
from ..models import Login
from .. import db


auth = Blueprint('auth', __name__)

def get_user():
    username = request.headers.get('Authorization')
    if username:
        user = Login.query.filter_by(username=username).first()
        return user
    return None

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
    data = request.get_json()
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
    
# Update credentials 
@auth.route('/update', methods={'POST'})
def update():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    current_user = get_user()
    if current_user is None:
        return jsonify({'error': 'Authentication required. Please log in'}), 401
    
    changes_made = False

    if password:
        current_user.password = password
        changes_made = True

    if username:
        current_user.username = username
        changes_made = True

    if changes_made: 
        try:
            db.session.commit()
            return jsonify({'message': 'Profile updated successfully!', 'new_username': current_user.username}), 200
        except Exception:
            db.session.rollback()
            return jsonify({'error': 'Failed to save changes to database'}), 500

@auth.route('/delete', methods={'DELETE'})
def delete():
    current_user = get_user()

    if current_user is None:
        return jsonify({'error': 'Not able to delete account'}), 400

    db.session.delete(current_user)
    db.session.commit()
    return jsonify({'message': 'Account deleted successfully'}), 200
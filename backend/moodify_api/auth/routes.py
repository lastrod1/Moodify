from flask import Blueprint, jsonify

auth = Blueprint('auth', __name__)

@auth.route('/mental')
def test():
    return {"members": ["funky", "donkey", "diddy"]}
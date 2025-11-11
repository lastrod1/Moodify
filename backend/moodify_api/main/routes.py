# Add stuff for CRUD functionality
from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/members')
def test():
    return {"members": ["funky", "donkey", "diddy"]}

@main.route('/')
def hello():
    return "hello"
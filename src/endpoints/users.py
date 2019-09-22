import json
from flask import Blueprint, request, Response
import os

from src.schema.user import User


bp = Blueprint('users', __name__)


@bp.route('/users/sign_up', methods=['POST'])
@bp.route('/api/users/sign_up', methods=['POST'])
def sign_up():
    """
    (POST): Create a new user

    Parameters:
        email (str): email to sign up with
        password (str): password to use (hashed w/ bcrypt)

    Example:
        curl -X POST /users/sign_up --data '{"email": "test@email.com", "password": "password123"}' -H 'Content-Type: application/json'

    Example response:
        {
            status: 'OK'
        }
    """
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return Response('Email and password is required', status=401, mimetype='application/json')

    if User.select().where(User.email == email).first():
        return Response('Email already taken', status=409, mimetype='application/json')

    encrypted_password = User.get_hashed_password(password)
    user = User.create(email=email, encrypted_password=encrypted_password)

    return Response(status=201)

@bp.route('/users/sign_in', methods=['PUT'])
@bp.route('/api/users/sign_in', methods=['PUT'])
def sign_in():
    """
    (PUT): Sign in

    Parameters:
        email (str): email to sign up with
        password (str): password

    Example:
        curl -X PUT /users/sign_in --data '{"email": "test@email.com", "password": "password123"}' -H 'Content-Type: application/json'

    Example response:
        'ff8d2a27-4943-4993-b8d4-3c02be4a75f0'
    """
    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or password is None:
        return Response('Email and password is required', status=401, mimetype='application/json')

    user = User.select().where(User.email == email).first()

    if user == None:
        return Response('Email or password is incorrect', status=403, mimetype='application/json')

    if user.check_password(password):
        return Response(os.environ['SECRET'] ,status=200, mimetype='application/json')

    return Response(status=403)

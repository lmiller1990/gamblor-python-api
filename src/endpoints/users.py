import json
from flask import Blueprint, request, Response

from src.schema.user import User


bp = Blueprint('users', __name__)


@bp.route('/users/sign_up', methods=['POST'])
@bp.route('/api/users/sign_up', methods=['POST'])
def teams():
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

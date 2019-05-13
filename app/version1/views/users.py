"""Views for the users resource"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.version1.models.users import Users
from app.version1.utilities.validators import validate_data_signup

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('firstname', help="You must supply your first name", required=True)
parser.add_argument('lastname', help="You must supply your last name", required=True)
parser.add_argument('email', help="You must supply your email", required=True)
parser.add_argument('password', help="You must supply a password", required=True)
parser.add_argument('confirm', help="You must supply a confirmation for your password", required=True)

class RegisterUsers(Resource):
    """
    Class to handle registering users
    POST /api/v1/auth/signup -> Creates a new user
    """
    def post(self):
        """Route to handle creating users"""
        args = parser.parse_args()
        response = validate_data_signup(args)
        if response == "valid":
            return Users().reg_user(
                args['firstname'],
                args['lastname'],
                args['email'],
                args['password'],
                args['confirm'])
        return response

class LoginUsers(Resource):
    """
    Class to handle user login
    POST '/api/v1/auth/login' -> Logs in a user
    """
    def post(self):
        return Users().login_user(
            request.json['email'],
            request.json['password'],
        )
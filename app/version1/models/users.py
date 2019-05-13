"""handles all operations for creating and fetching data relating to users"""
import psycopg2
from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash


from app.version1.utilities.db import connection


class Helper():
    """Carries out common functions"""

    @staticmethod
    def json(data):
        return dict(email=data[4], firstname=data[1], lastname=data[2])


    def check_if_user_exists(self, email):
        """
        Helper function to check if a user exists
        Returns a message if a user already exists
        """
        try:
            connect = connection.dbconnection()
            cursor = connect.cursor(cursor_factory=RealDictCursor)
            cursor.execute("SELECT * FROM users WHERE email = '{}'".format(email))
            connect.commit()
            email = cursor.fetchone()
            cursor.close()
            connect.close()
            if email:
                return True
        except (Exception, psycopg2.DatabaseError) as error:
            return {'error' : '{}'.format(error)}, 401

class Users(Helper):
    """Class to handle users"""
    def reg_user(self, firstname, lastname, email, password, confirm):
        """Method to handle user creation"""
        firstname = request.json.get('firstname', None)
        lastname = request.json.get('lastname', None)
        email = request.json.get('email', None)
        password = request.json.get('password', None)
        confirm = request.json.get('confirm', None)

        # Check for empty inputs
        if firstname == '' or lastname == '' or email == '' or password == '' or confirm == '':
            return{
                "status": 401,
                "error": "Neither of the fields can be left empty"
                }, 401

        if password != confirm:
            return{
                "status": 401,
                "error": "The passwords do not match"
                }, 401


        if len(password) < 6 or len(password) > 12:
            return{
                "status": 401,
                "error": "Password length should be between 6 and 12 characters long"
                }, 401

        present = Helper.check_if_user_exists(self, email)
        if present:
            return{
                "status": 409,
                "error": "There is a user with the same email registered"
                }, 409

        try:
            hashed_password = generate_password_hash(password)
            add_user = "INSERT INTO \
                        users (firstname, lastname, email, password, isadmin) \
                        VALUES ('" + firstname +"', '" + lastname +"', '" + email +"', '" + hashed_password +"', false )"
            connect = connection.dbconnection()
            cursor = connect.cursor()
            cursor.execute(add_user)
            connect.commit()
            response = jsonify({'status': 201,
                                "msg":'User Successfully Created'})
            response.status_code = 201
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'status': 500,
                                'msg':'Problem fetching record from the database'})
            response.status_code = 500
            return response

    def login_user(self, email, password):
        """Logs in a user"""


        email = request.json.get('email', None)
        password = request.json.get('password', None)

        # Check for empty inputs
        if email == '' or password == '':
            return{
                "status": 401,
                "error": "Neither of the fields can be left empty during log in"
                }, 401

        try:
            get_user = "SELECT email, password, isadmin, user_id \
                        FROM users \
                        WHERE email = '" + email + "'" 
            connect = connection.dbconnection()
            cursor = connect.cursor(cursor_factory=RealDictCursor)
            cursor.execute(get_user)
            row = cursor.fetchone()
            if row is not None:
                access_token = create_access_token(identity=dict(email=row["email"], id=row['user_id']))
                valid = check_password_hash(row.get('password'), password)
                if valid:
                    response = jsonify({
                        "user":{
                            'email':row['email']
                            },
                        "success":"User Successfully logged in", 
                        "access_token":access_token})
                    response.status_code = 200
                    return response
            response = jsonify({"status": 401,
                "msg" : "Error logging in, credentials not found"})
            response.status_code = 401
            return response
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            response = jsonify({'status': 500,
                                'msg':'Problem fetching record from the database'})
            response.status_code = 500
            return response
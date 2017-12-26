from flask_restful import Resource, reqparse
from flask import Blueprint, request, Response
from jinja2 import TemplateNotFound
from hswebapp import app,db
#from importlib import import_module

from datetime import datetime
from time import sleep

from werkzeug.security import generate_password_hash,check_password_hash
from hswebapp.models.system_models import User,Logs
import copy
from hswebapp.api import apiv0

#GET /api/users/<id> Return a user.
#GET /api/users Return the collection of all users.
#GET /api/users/<id>/followers Return the collection of followers of this user.
#GET /api/users/<id>/followed Return the collection of users this user is following.
#POST /api/users Register a new user account. User representation given in the body.
#PUT /api/users/<id> Modify a user. Only allowed to be issued by the user itself.

@apiv0.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    pass









class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

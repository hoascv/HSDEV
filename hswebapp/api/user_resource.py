from flask_restful import Resource, reqparse
from flask import Blueprint, request, Response,jsonify
from jinja2 import TemplateNotFound
from hswebapp import app,db
#from importlib import import_module

from datetime import datetime
from time import sleep

from werkzeug.security import generate_password_hash,check_password_hash
from hswebapp.models.system_models import User,Logs
import copy
from hswebapp.api import apiv0
from hswebapp.api.auth import token_auth

#GET /api/users/<id> Return a user.
#GET /api/users Return the collection of all users.
#GET /api/users/<id>/followers Return the collection of followers of this user.
#GET /api/users/<id>/followed Return the collection of users this user is following.
#POST /api/users Register a new user account. User representation given in the body.
#PUT /api/users/<id> Modify a user. Only allowed to be issued by the user itself.


@apiv0.route('/apiv1/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):

    return jsonify(User.query.get_or_404(id).to_dict(True))
    #user = User.query.get(int(id))
    #return user.to_dict()

@apiv0.route('/apiv1/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 2, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'apiv0.get_users')
    return jsonify(data)









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

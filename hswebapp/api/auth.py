from hswebapp.models.system_models import User
from flask import g,jsonify
from flask_httpauth import HTTPBasicAuth

basic_auth= HTTPBasicAuth()



@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    #return error_response(401)
    return jsonify({"message": "Authentication error"}),401



##TODO: https://flask-httpauth.readthedocs.io/en/latest/    

from hswebapp.models.system_models import User
from flask import g,jsonify
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from hswebapp import app,db

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()
 


@basic_auth.verify_password
def verify_password(username, password):
    try:
        user = User.query.filter_by(username=username).first()
        if user is None:
            return False
    except Exception as e:
        app.logger.error('verify password api error: {}'.format(e))
        raise
        db.session.rollback()
        
    finally:
        db.session.close()
    
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    #return error_response(401)
    return jsonify({"message": "Authentication error"}),401

@token_auth.verify_token
def verify_token(token):
    g.current_user = User.check_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return jsonify({"message": "Invalid Token"}),401
    
    
##add @token_auth.login_required
    
    

##TODO: https://flask-httpauth.readthedocs.io/en/latest/    

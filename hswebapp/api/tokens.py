from flask import jsonify,g
#from hswebapp import db
from hswebapp.api import apiv0
from hswebapp.api.auth import basic_auth,token_auth


@apiv0.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    return jsonify({'token':token})

@apiv0.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    return jsonify({'user':g.current_user.username}), 204


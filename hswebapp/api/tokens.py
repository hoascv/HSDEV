from flask import jsonify,g
#from hswebapp import db
from hswebapp.api import apiv0
from hswebapp.api.auth import basic_auth,token_auth
from hswebapp.models.system_models import Logs
from hswebapp import db


@apiv0.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    log = Logs(user_id= g.current_user.id,operation='login',origin='api')
    db.session.add(log)
    db.session.commit()
    return jsonify({'token':token,'expire in':g.current_user.token_expiration })

@apiv0.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    log = Logs(user_id= g.current_user.id,operation='logout',origin='api')
    db.session.add(log)
    db.session.commit()
    return jsonify({'user':g.current_user.username}), 204


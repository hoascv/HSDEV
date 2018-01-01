from flask import jsonify,g
#from hswebapp import db
from hswebapp.api import apiv0
from hswebapp.api.auth import basic_auth


@apiv0.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    return jsonify({'token':token})

def revoke_token():
   pass


from flask import Blueprint
wst = Blueprint('wst',__name__,template_folder='templates/pages')
from hswebapp.ws import streaming

import os,sys
from flask import Flask,render_template,current_app
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler

from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from datetime import datetime
from blinker import Namespace
from flask_marshmallow import Marshmallow

from flask_migrate import Migrate


 


#basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

app.config.from_pyfile('config/config.py')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app,db)



@app.before_first_request
def create_tables():
    db.create_all()

login_manager = LoginManager(app) 
login_manager.login_view = 'webapp_auth.login'



my_signals = Namespace()
model_saved = my_signals.signal('model-saved')


    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))   



handler = RotatingFileHandler('/var/www/hswebapp/log/app/hswebapp.log', maxBytes=100000, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


#log sqlalchemy test

#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

#sys.stdout



from hswebapp.views import views
app.register_blueprint(views)

from hswebapp.ws import wst
app.register_blueprint(wst)


from hswebapp.auth import webapp_auth
app.register_blueprint(webapp_auth)

from hswebapp.system import system
app.register_blueprint(system)

from hswebapp.models.system_models import system_models,User 
app.register_blueprint(system_models)

from hswebapp.api import apiv0  
app.register_blueprint(apiv0,url_prefix='/api')



#app.logger.info('end init')
#from hswebapp.resources import u

@app.shell_context_processor
def make_shell_context():
    return{'db':db,'User':User}

	

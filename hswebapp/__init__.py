import os,sys
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
#testing
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,UserMixin
from datetime import datetime
 


#basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

app.config.from_pyfile('config/config.py')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager(app) 
login_manager.login_view = 'views.login'

class User(UserMixin,db.Model): ## move class User to models.py 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email= db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    isadmin = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastlogin = db.Column(db.DateTime)
    acesslevel =db.Column(db.Integer)
    
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))   



handler = RotatingFileHandler('/var/www/hswebapp/hswebapp/log/hswebapp.log', maxBytes=100000, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)








from hswebapp.views import views
app.register_blueprint(views)
from hswebapp.webstreaming import webstreaming
app.register_blueprint(webstreaming)
#app.logger.info('end init')
#from hswebapp.resources import u


	

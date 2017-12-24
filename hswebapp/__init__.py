import os,sys
from flask import Flask,render_template,current_app
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
#testing
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,UserMixin
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
login_manager.login_view = 'views.login'



my_signals = Namespace()

model_saved = my_signals.signal('model-saved')


class User(UserMixin,db.Model): ## move class User to models.py 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email= db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    isadmin = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastlogin = db.Column(db.DateTime)
    acesslevel =db.Column(db.Integer)
    
    def __repr__(self):
        return "<User(name='%s', createdAt='%s')>" % (
                             self.username, self.createdAt)   
    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))   



handler = RotatingFileHandler('/var/www/hswebapp/log/app/hswebapp.log', maxBytes=100000, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)








from hswebapp.views import views
app.register_blueprint(views)

from hswebapp.webstreaming import webstreaming
app.register_blueprint(webstreaming)


from hswebapp.auth import auth
app.register_blueprint(auth)

from hswebapp.system import system
app.register_blueprint(system)




#app.logger.info('end init')
#from hswebapp.resources import u


	

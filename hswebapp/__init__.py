import os,sys
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
#from hswebapp.config import DbConfig


#basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

app.config.from_object('config.config_app.DbConfig')
#configure database
#app.config["DEBUG"] = True 
#app.config['SECRET_KEY']=",\x80\xa9G\xcb\xc7W\x1c\x10*6\xd5\xc3,'zi.c\xb2\xf0\x81(\x15" 
#SQLALCHEMY_DATABASE_URI ="mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
#    username="root",
#    password="thomasmaximus",
#    hostname="localhost",
#    databasename="hswebapp_db", ) 
#app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI 
#app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#import models
#end of models

from hswebapp.views import views
app.register_blueprint(views)
from hswebapp.webstreaming import webstreaming
app.register_blueprint(webstreaming)
#from hswebapp.resources import u

	

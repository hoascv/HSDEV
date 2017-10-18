import os,sys
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy



#basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

app.config.from_pyfile('config/config.py')
db = SQLAlchemy(app)

#import models
#end of models

from hswebapp.views import views
app.register_blueprint(views)
from hswebapp.webstreaming import webstreaming
app.register_blueprint(webstreaming)
print ('end init')
#from hswebapp.resources import u

	

import os,sys
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
#testing
from flask_bootstrap import Bootstrap




#basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

app.config.from_pyfile('config/config.py')

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


handler = RotatingFileHandler('/var/www/hswebapp/hswebapp/log/hswebapp.log', maxBytes=100000, backupCount=10)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)








from hswebapp.views import views
app.register_blueprint(views)
from hswebapp.webstreaming import webstreaming
app.register_blueprint(webstreaming)
#app.logger.info('end init')
#from hswebapp.resources import u


	

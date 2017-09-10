from models.templog import TempLog
from models.humiditylog import HumidityLog
from db import db

app.config["DEBUG"] = True app.config['SECRET_KEY']=",\x80\xa9G\xcb\xc7W\x1c\x10*6\xd5\xc3,'zi.c\xb2\xf0\x81(\x15" 
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="thomasmaximus",
    hostname="localhost",
    databasename="hswebapp_db", )
	
app.config["SQLALCHEMY_DATABASE_URI"] =SQLALCHEMY_DATABASE_URI app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db= SQLAlchemy(app) 
db.create_all()


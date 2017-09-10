import os,sys
from datetime import datetime
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import sys
import Adafruit_DHT









app = Flask(__name__)

#configure database
app.config["DEBUG"] = True 
app.config['SECRET_KEY']=",\x80\xa9G\xcb\xc7W\x1c\x10*6\xd5\xc3,'zi.c\xb2\xf0\x81(\x15" 
SQLALCHEMY_DATABASE_URI ="mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="thomasmaximus",
    hostname="localhost",
    databasename="hswebapp_db", ) 
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI 
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#import models
class HumidityLog(db.Model):
    __tablename__ = 'humiditylog'

    id = db.Column(db.Integer, primary_key= True)
    data = db.Column(db.Date)
    sensorLocation = db.Column(db.String(5))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(10))
    
    def __init__ (self,data,sensorLocation,sensorType,value):
        self.data = data
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    @classmethod
    def find_by_sensorLocation(cls,sensorLocation):
        return cls.query.filter_by(sensorLocation=sensorLocation)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
 
 
class TempLog(db.Model):
    __tablename__ = 'templog'

    id     = 		db.Column(db.Integer, primary_key= True)
    data   = 		db.Column(db.Date)
    sensorLocation =	db.Column(db.String(5))
    value  = 		db.Column(db.Float(precision=2))
    sensorType = 	db.Column(db.String(10))
    
    def __init__(self,data,sensorLocation,sensorType,value):
        self.data = data
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    @classmethod
    def find_by_sensorLocation(cls,sensorLocation):
        return cls.query.filter_by(sensorLocation=sensorLocation)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 22)
if humidity is not None and temperature is not None:
    reading = TempLog(datetime.now(),'livingroom','dht22',temperature)
    reading.save_to_db()
    readingH= HumidityLog(datetime.now(),'livingroom','dht22',humidity)
    readingH.save_to_db()



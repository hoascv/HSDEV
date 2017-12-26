from flask import Blueprint,render_template,flash, redirect, url_for, request, Response
from jinja2 import TemplateNotFound
from datetime import datetime
from hswebapp import db,model_saved,ma
from marshmallow import fields
from flask_login import LoginManager,UserMixin

system_models = Blueprint('system_models', __name__,template_folder='templates/system')



class User(UserMixin,db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email= db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    isadmin = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastlogin = db.Column(db.DateTime)
    acesslevel =db.Column(db.Integer)
    logs = db.relationship('Logs', backref='log_history', lazy='dynamic')
    
    def __repr__(self):
        return "<User(name='%s', createdAt='%s')>" % (
                             self.username, self.createdAt)   

                             
class Logs(db.Model):
    id      = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    operation =db.Column(db.String(10))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    
    def __init__ (self,operation,user_id):
        self.operation=operation
        self.user_id=user_id
        
    def __repr__(self):
        return "<Log date: {} operation: {} User: {}".format(self.timestamp,self.operation,self.user_id)
        


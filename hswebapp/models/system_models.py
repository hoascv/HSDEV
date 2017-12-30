from flask import Blueprint,render_template,flash, redirect, url_for, request, Response
from jinja2 import TemplateNotFound
from datetime import datetime
from hswebapp import db,model_saved,ma
from marshmallow import fields
from flask_login import LoginManager,UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

system_models = Blueprint('system_models', __name__,template_folder='templates/system')



class User(UserMixin,db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email= db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    isadmin = db.Column(db.Boolean)
    createdAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,onupdate=datetime.utcnow)
    lastlogin = db.Column(db.DateTime)
    isActivated = db.Column(db.Boolean,default=False)
    acess_group = db.Column(db.Integer,db.ForeignKey('access_group.id'))
    deleted_on= db.Column(db.DateTime, default=datetime.utcnow)
    
    
    
    
    logs = db.relationship('Logs', backref='log_history', lazy='dynamic')
    
    def __repr__(self):
        return "<User(name='%s', createdAt='%s')>" % (
                             self.username, self.createdAt)   

    def to_dict(self,include_sensitivedata=False):
        data={
            'id':self.id,
            'username':self.username,
            'lastlogin':self.lastlogin,
            'last_updated':self.updatedAt,
            'logs':self.logs.count(),
            '_links': {
                'self':url_for('apiv0.get_user',id=self.id),
                'obs':'add more links'
            }
        }
        if include_sensitivedata :
            data['email'] = self.email
        return data
        
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])    
 
    def set_password(self,new_password):
        self.password=generate_password_hash(new_password,method='sha256')
    
    def check_password(self,check_password):
        return check_password_hash(self.password,check_password)    


    
class AccessGroup(db.Model):
    __tablename__ = 'access_group'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String(15), unique = True)
    users = db.relationship('User',backref='user_group', lazy='dynamic')                        
    
    def __repr__(self):
        return "<Group (name={})".format(self.description)
        
                             
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
        


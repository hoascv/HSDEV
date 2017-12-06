from hswebapp import db
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField
from  wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=80)])
    advanceuser = BooleanField('Advance User')

class AdminForm(LoginForm): ##Todo 
    isadmin = BooleanField('isAdmin')
    acesslevel = StringField('Acess Level', validators=[InputRequired(),Length(min=1,max=1)])    
    
    
    
class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=15)])
    email    = StringField('email',  validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=80)])
    advanceduser = BooleanField('Advanced User')
  
    
    
    
class ServerMgmt(FlaskForm):
    reason = StringField('Reason',validators=[InputRequired(),Length(min=4,max=15)])
    code = PasswordField('Code',validators=[InputRequired(),Length(min=4,max=6)])
    #date = StringField('Date',validators=[InputRequired(),Length(min=4,max=15)])
    
    
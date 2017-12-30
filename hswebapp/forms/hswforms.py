from hswebapp import db
from flask_wtf import FlaskForm
from wtforms import Form, StringField,PasswordField,BooleanField,DateTimeField,validators,IntegerField,ValidationError,SubmitField,SelectField
from  wtforms.validators import InputRequired, Email, Length

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=15)])
    password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=80)])
    rememberme = BooleanField('Remember me')

class AdminForm(LoginForm): ##Todo 
    isadmin = BooleanField('isAdmin')
    acesslevel = IntegerField('Acess Level [1-3]', validators=[InputRequired(),Length(min=1,max=1)])    
    
    def validate_accesslevel(form, field):
        if field.data  <= 1:
            raise ValidationError("Acess level must be greater then 1 ")

    
    
    
#class RegisterForm(FlaskForm):
#    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=15)])
#    email    = StringField('email',  validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
#    password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=80),EqualTo('confirm', message='Passwords must match')])
#    confirm = PasswordField('Repeat Password')
#    advanceduser = BooleanField('Advanced User')        

class RegisterForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    advanceduser = BooleanField('Advanced User')
    
        
    
class ServerMgmt(FlaskForm):
    reason = StringField('Reason',validators=[InputRequired(),Length(min=4,max=15)])
    code = PasswordField('Code',validators=[InputRequired(),Length(min=4,max=6)])
    #date = StringField('Date',validators=[InputRequired(),Length(min=4,max=15)])
    
    
class EditUserForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired(),Length(min=4,max=15)])
    #password = PasswordField('Password', validators=[InputRequired(),Length(min=4,max=80)])
    email = StringField('Email Address', validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    isadmin = BooleanField('is Admin')
    createdAt = DateTimeField('Created At:')
    updatedAt = DateTimeField('updated At:')
    lastlogin = DateTimeField('Last login:')
    isActivated =BooleanField('IsActivated')
    acess_group =SelectField('Access Group',coerce=int)
    #http://wtforms.simplecodes.com/docs/0.6/fields.html
    submit = SubmitField('Update')
    
from flask import Blueprint,render_template,flash, redirect, url_for, request, Response
from jinja2 import TemplateNotFound
from hswebapp import app,db
from importlib import import_module
import os
from flask_login import login_required,login_user,logout_user, current_user


auth = Blueprint('auth', __name__,template_folder='templates\auth')


@auth.route('/login_1')
@login_required
def login_1():
    pass
    return 1

from flask import Blueprint,render_template,flash, redirect, url_for, request, Response
from jinja2 import TemplateNotFound
from hswebapp import app,db
from importlib import import_module
import os
from flask_login import login_required,login_user,logout_user, current_user
from hswebapp.models.hsutil import Hsutil
from datetime import datetime
from time import sleep

system = Blueprint('system', __name__,template_folder='templates/system')


@system.route('/system', methods=["GET"])
@login_required
def system_info():
    import psutil
    
    return render_template("system.html",psuvar=psutil,hsutil = Hsutil)    

    
@system.route('/shutdown',  methods=['POST'])
@login_required
def shutdown():
    import subprocess
     
    reason = request.form['reason']
    app.logger.info(reason)
    
    code = request.form['code']   
    app.logger.info(code)
    
    if (code == "HSS"):    
        message = "Shutdown initiated at  {} ".format(datetime.now())
        flash(message)
        app.logger.info(message)  
        #cmd = ["ls","-l"]
        cmd = ["shutdown"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        flash("Code invalid")
        return redirect(url_for('home'))
        
        
@system.route('/srvmng/<int:option>')
@login_required
def srvmng(option):
    
    return render_template("srvmng_page.html",option=option)    
   

@system.route('/reboot',  methods=['POST'])
def reboot():
    import subprocess
     
    reason = request.form['reason']
    app.logger.info(reason)
    
    code = request.form['code']   
    app.logger.info(code)
    if (code == "HSR"):      
        message = "Restart initiated at  {} ".format(datetime.now())
        flash(message)
        app.logger.info(message) 
        sleep(20)
    #cmd = ["ls","-l"]
        cmd = ["reboot"]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
        out,err = p.communicate()
        return out
    else:
        flash("Code Invalid")
        return redirect(url_for('home'))
    
@system.route('/command',  methods=['GET'])  
def command():

    cmd = ["iwconfig"]
    
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    
    out,err = p.communicate()
    
    return out
    
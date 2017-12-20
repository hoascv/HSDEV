from flask import Blueprint,render_template,flash, redirect, url_for, request, Response,Flask,jsonify
from jinja2 import TemplateNotFound
from hswebapp import app,db,login_manager,User,model_saved
from hswebapp.models.models import TempLog,HumidityLog,PressureLog,PowerLog,sensorlog_schema,powerlog_schema,EventLog
from hswebapp.models.hsutil import Hsutil
from hswebapp.forms.hswforms import LoginForm,RegisterForm
import subprocess
from datetime import datetime
from time import sleep
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_required,login_user,logout_user, current_user






views = Blueprint('views', __name__,template_folder='templates')

signals_events = []
##teste

from marshmallow import pprint



def add_event(message):
    return message
 
  #  print(len(signals_events)) 
    
#signals_events.append(add_event)



  
  
    
    
#@login_manager.user_loader
#def load_user(user_id):
#    print('print views')
#    return User.query.get(int(user_id))    

    
    
    
    
    
@views.route('/')
def home():
    return render_template('pages/home.html')


@views.route("/environment")
@login_required
def dashboard():
    import sys
 
    try:
                       
            temperature_sensor1= TempLog.query.order_by(TempLog.rdate.desc()).filter_by(sensorType='AM2302').first()          
            temperature_sensor2= TempLog.query.order_by(TempLog.rdate.desc()).filter_by(sensorType='DH11').first()                        
            temperature_sensor3= TempLog.query.order_by(TempLog.rdate.desc()).filter_by(sensorType='BMP180').first()
                        
            humidity_sensor1= HumidityLog.query.order_by(HumidityLog.rdate.desc()).filter_by(sensorType='AM2302').first()     
            humidity_sensor2= HumidityLog.query.order_by(HumidityLog.rdate.desc()).filter_by(sensorType='DH11').first()        
                        
            pressure_sensor1= PressureLog.query.order_by(PressureLog.rdate.desc()).first()
            
            power_sensor1 =   PowerLog.query.order_by(PowerLog.rdate.desc()).first()
                     
                         

    except:
        flash("InvalidRequestError: {} ".format(sys.exc_info()[0]))
        
        raise
        db.session.rollback()
        return redirect(url_for('home'))
    finally:
        db.session.close()
     
    
    return render_template("pages/dashboard.html",temperature_sensor1=temperature_sensor1,
                                temperature_sensor2=temperature_sensor2,
                                temperature_sensor3=temperature_sensor3,
                                humidity_sensor1=humidity_sensor1,
                                humidity_sensor2=humidity_sensor2,
                                pressure_sensor1=pressure_sensor1,
                                power_sensor1=power_sensor1,
                                TempLog=TempLog,
                                HumidityLog=HumidityLog,
                                PressureLog=PressureLog,
                                PowerLog=PowerLog
                                )
  
        
@views.route('/readings', methods=["GET"])
@login_required
def report_listreadings():

   # if request.method == "GET": 
    
    return render_template("readings.html", temperature = TempLog.query.order_by(TempLog.rdate.desc()).limit(50).all(), humidity = HumidityLog.query.order_by(HumidityLog.rdate.desc()).limit(50).all(), pressure = PressureLog.query.order_by(PressureLog.rdate.desc()).limit(50).all(), power = PowerLog.query.order_by(PowerLog.rdate.desc()).limit(50).all())
               

@views.route('/grafics', methods=["GET"])
def report_grafics():
    import sys
    import Adafruit_DHT
    import Adafruit_BMP.BMP085 as BMP085
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 23)
    values_sensor = BMP085.BMP085()

    try:
            #query_result = db.engine.execute('select count(id) as num from templog')
            #for row in query_result:
            #    result= row['num']
                            
            result=TempLog.query.count()
            #templog = db.session.query(TempLog).all()
            templog= TempLog.query.order_by(TempLog.rdate.desc()).limit(10).all()
            humiditylog= HumidityLog.query.order_by(HumidityLog.rdate.desc()).limit(10).all()
            pressurelog= PressureLog.query.order_by(PressureLog.rdate.desc()).limit(10).all()
            powerlog =   PowerLog.query.order_by(PowerLog.rdate.desc()).limit(10).all()
        
        
    except:
        app.logger.error("InvalidRequestError: {} ".format(sys.exc_info()[0]))
        
        raise
        db.session.rollback()
        return redirect(url_for('home'))
    finally:
        db.session.close()
        
         
    
    #db.session.close()
    
    if humidity is not None and temperature is not None and values_sensor is not None:
        return render_template("pages/grafics.html",ntemp=result,
                                temperature=temperature,temp = templog,
                                humidity=humidity,humididylog= humiditylog,
                                pressure=float(values_sensor.read_pressure()/100),
                                pressurelog=pressurelog,
                                powerlog=powerlog
                                )
    else:
        return render_template("no_sensor.html")
         
      
@views.route('/system', methods=["GET"])
@login_required
def system():
    import psutil
    
    return render_template("pages/system.html",psuvar=psutil,hsutil = Hsutil)    

    
@views.route('/shutdown',  methods=['POST'])
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
        return render_template('pages/home.html')
        
        
@views.route('/srvmng/<int:option>')
@login_required
def srvmng(option):
    
    return render_template("pages/srvmng_page.html",option=option)    
   

@views.route('/reboot',  methods=['POST'])

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
        return render_template('pages/home.html')
    
@views.route('/command',  methods=['GET'])  
def command():

    cmd = ["iwconfig"]
    
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    
    out,err = p.communicate()
    
    return out
    
    
@views.route('/about1', methods=["GET"])
@login_required
def about1():
    return render_template("pages/about.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"),404

    
     
    
@views.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data,method='sha256')
                
        try:
            new_user = User(username=form.username.data,email=form.email.data,password=hashed_password,lastlogin=datetime.now())
            db.session.add(new_user)
            db.session.commit()
            
        except IntegrityError as e:
            db.session.rollback()
            flash('The user: {} or the email {} already exists \n Thank you'.format(form.username.data,form.email.data))
            app.logger.error('Sign up error: {}'.format(e))
            return render_template("pages/hsw_signup.html",form = form)
        
        except Exception as e:
            app.logger.error('Sign up error: {}'.format(e))
            db.session.rollback()
            flash('Error! Sorry for the inconvinience The issue has been logged and it will be solved asap')
            return render_template("pages/hsw_signup.html",form = form)
            
        flash('The user: {} has been created'.format(form.username.data))                
        return redirect(url_for('views.login'))
        
    return render_template("pages/hsw_signup.html",form = form)

@views.route('/login', methods=['GET','POST'] )
def login():
    form = LoginForm()
    if form.validate_on_submit():
    
            
        user = User.query.filter_by(username=form.username.data).first()
        if (user):
            if check_password_hash(user.password,form.password.data):
                user.lastlogin = datetime.now()
                db.session.commit()
                
                login_user(user,remember=form.rememberme.data)
                #TODO IMPLEMENT REDIRECT GET THE NEXT
                #next = request.args.get('next')
                #if not is_safe_url(nextform):
                #    return flask.abort(400)
                #http://flask.pocoo.org/snippets/62/
                #return redirect(url_for(next))
                return redirect(url_for('views.home'))
            
            flash('Invalid password')
            return render_template("pages/hsw_login.html",form = form)
        flash('User does not exist')
        return render_template("pages/hsw_login.html",form = form)
    
    return render_template("pages/hsw_login.html",form = form)

@views.route('/logout')
@login_required
def logout():
       
    logout_user()
    flash("See ya")
    return redirect(url_for('views.home'))
    
    
    
@views.route('/users')
@login_required
def system_users():
    users = User.query.all()
    return render_template('pages/system_users.html', users=users)
    

@views.route('/update_user', methods=['POST'])
@login_required
def update_user():
    app.logger.info('updating user')
    updated=datetime.now()
    try:
        user = User.query.filter_by(id=request.form['id']).first()
        user.username = request.form['username']
        user.email = request.form['email']
        user.updatedAt = updated
        
        db.session.commit()
        
    
    except Exception as e:
        app.logger.error('Update error: {}'.format(e))
        db.session.rollback()
        flash('Error! Sorry for the inconvinience The issue has been logged and it will be solved asap') 
        return jsonify({'result' : 'error'})
    
    finally:
        db.session.close()
        
    return jsonify({'result' : 'success', 'updated' :updated })



    
@model_saved.connect
def model_saved_signal(app, message, **extra):
#check what page/template is beind rendered
    event=EventLog(ob_id=message.get_id(), ob_type=message.get_type())
    event.save_to_db()
    
 
    
    

@views.route('/update_dashboard', methods=['POST'])
@login_required
def update_dashboard():
    
    
    
    page_load=(request.form['page_load']) 
    
    fmt="YYYY-mm-ddTHH:MM:SS.SSSZ"
    py_format='YYYY-MM-DDTHH:MM:SS'
    
    
    
    jsdate=datetime.strptime(page_load, '%Y-%m-%dT%H:%M:%S.%fZ')
    
    
    #ValueError: time data '2017-12-17T20:46:23.438Z' does not match format 'YYYY-MM-DDTHH:MM:SS'
    #datetime_object = datetime.strptime(page_load,py_format)
    print('##############date###################')
    print(jsdate)
    print('##############date###################')        
    #now_utc = datetime.now(timezone('UTC'))
    
    try:
        if  (EventLog.query.count()==0) :
            return jsonify({'result' : 'no_data','last_Attempt': datetime.now()})
        else: 
            event = EventLog.query.order_by(EventLog.id.asc()).first()
        
        
    except:
        app.logger.error("InvalidRequestError: {} ".format(sys.exc_info()[0]))
        
        raise
        db.session.rollback()
        return jsonify({'result' : 'no_data','last_Attempt': datetime.now()})
    finally:
        db.session.close()
 
            
    if (event.ob_type=='TempLog'):
        updated=TempLog.query.filter_by(id=event.ob_id).first()
      
    elif (event.ob_type=='HumidityLog'):
        updated=HumidityLog.query.filter_by(id=event.ob_id).first()   
    elif (event.ob_type=='PressureLog'):
        updated=PressureLog.query.filter_by(id=event.ob_id).first()   
    elif (event.ob_type=='PowerLog'):
        updated=PowerLog.query.filter_by(id=event.ob_id).first() 

    event.delete_from_db()
        
        
        
    if (type(updated) is PowerLog):
        result = powerlog_schema.dump(updated)
        return poewrlog_schema.jsonify(updated)
    else :
        result = sensorlog_schema.dump(updated)
        pprint(result)
        return sensorlog_schema.jsonify(updated)
        

@views.route('/update_event', methods=['POST'])
@login_required
def dashboard_event():
    pass
    
# retreive the the time that the page has been loaded and return the next event_id to be refreshed
# 


    
    
    
from flask import Blueprint,render_template,flash, redirect, url_for, request, \
                  Response,Flask,jsonify,session
from jinja2 import TemplateNotFound
from hswebapp import app,db,login_manager,model_saved,celery
from hswebapp.models.sensor_models import TempLog,HumidityLog,PressureLog,PowerLog,EventLog
from hswebapp.models.resources import sensorlog_schema,powerlog_schema,templog_schema
from datetime import datetime
#testing 
from random import randint

from flask_mail import Mail,Message
mail = Mail(app)

#from sqlalchemy.exc import IntegrityError
from flask_login import login_required,login_user,logout_user, current_user
from hswebapp.models.system_models import User

#####
import requests
import json

views = Blueprint('views', __name__,template_folder='templates')


def add_event(message):
    return message
   
    
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
    try:
        temperature = TempLog.query.order_by(TempLog.rdate.desc()).limit(50).all()
        humidity = HumidityLog.query.order_by(HumidityLog.rdate.desc()).limit(50).all()
        pressure = PressureLog.query.order_by(PressureLog.rdate.desc()).limit(50).all()
        power = PowerLog.query.order_by(PowerLog.rdate.desc()).limit(50).all()
    
    except:
        flash("InvalidRequestError: {} ".format(sys.exc_info()[0]))
        
        raise
        db.session.rollback()
        return redirect(url_for('home'))
    finally:
        db.session.close()
        
   
    return render_template("readings.html", temperature = temperature,humidity =humidity, pressure = pressure, power = power)
               

@views.route('/grafics', methods=["GET"])
def report_grafics():
    import sys
    try:
        result=TempLog.query.count()
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
        
        
    return render_template("pages/grafics.html",ntemp=result,
                                temp = templog,
                                humididylog= humiditylog,
                                pressurelog=pressurelog,
                                powerlog=powerlog
                                )
   
    
@views.route('/about1', methods=["GET"])
@login_required
def about1():
    return render_template("pages/about.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"),404

    
@model_saved.connect
def model_saved_signal(app, message, **extra):
#check what page/template is beind rendered
    
    try:
        event=EventLog(ob_id=message.get_id(), ob_type=message.get_type())
        event.save_to_db()
    
    except Exception as e:
        app.logger.error('Update error: {}'.format(e))
        db.session.rollback()
    
    finally:
        db.session.close()
    
 
@views.route('/update_dashboard', methods=['POST'])
@login_required
def update_dashboard():
      
    page_load=(request.form['page_load']) 
    
    fmt="YYYY-mm-ddTHH:MM:SS.SSSZ"
    py_format='YYYY-MM-DDTHH:MM:SS'    
    jsdate=datetime.strptime(page_load, '%Y-%m-%dT%H:%M:%S.%fZ')
        
    #ValueError: time data '2017-12-17T20:46:23.438Z' does not match format 'YYYY-MM-DDTHH:MM:SS'
    #datetime_object = datetime.strptime(page_load,py_format)
    #print('##############date###################')
    #print(jsdate)
    #print('##############date###################')        
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
        return powerlog_schema.jsonify(updated)
    else :
        result = sensorlog_schema.dump(updated)
        #pprint(result)
        return sensorlog_schema.jsonify(updated)
        

@views.route('/update_event', methods=['POST'])
@login_required
def dashboard_event():
    pass    
# retreive the the time that the page has been loaded and return the next event_id to be refreshed



@views.route('/exporting_templog')
@login_required
def exporting():
    
    #op = randint(0,1)
    sensor_type = request.args.get('sensor_type', 'PressureLog', type=str)
    sensor_class = globals()[sensor_type]     
        
        
    try:
        
       
        log = sensor_class.query.with_for_update().filter(sensor_class.exported.is_(None)).order_by(sensor_class.rdate.desc()).first()
               
            
        if (log is None): 
            return jsonify({'message':'no_data'}),204
        else :
            mdata= templog_schema.dump(log).data
    
    except Exception as e:
        app.logger.error('Error reading bd : {}'.format(e))
        db.session.rollback()
    
    finally:
        db.session.close()
    
    
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    #r = requests.post('https://dev.hswebapp.com/api/templog', data = {'key':'value'})    
    my_request = requests.post('https://dev.hswebapp.com/api/templog?sensor_type='+sensor_type,json=mdata,headers=headers)              
    
    if (my_request.status_code == 201 or my_request.status_code == 409):
        log.exported = datetime.utcnow()
        db.session.add(log)
        db.session.commit()
    
    
    
    #print(my_request.status_code)
    print(my_request.json())
    if (my_request.status_code != 201 ):
        return jsonify(my_request.json()),my_request.status_code
    
    return jsonify(my_request.json()),201

@views.route('/export')
@login_required
def export(): 
    
    return render_template('pages/export.html',TempLog=TempLog,HumidityLog=HumidityLog,PressureLog=PressureLog)
   
   
   
@views.route('/test99')
@login_required
def send_mail():
    
    
    session['email'] = 'hoascv@gmail.com'
    
    # send the email
    msg = Message('Hello from Flask',sender='hsupp99@gmail.com',
                  recipients=['hoascv@gmail.com'])
    msg.body = 'This is a test email sent from a background Celery task.'
    send_async_email.delay(msg)
    return redirect(url_for('home'))    
@celery.task
def send_async_email(msg):
    """Background task to send an email with Flask-Mail."""
    with app.app_context():
        mail.send(msg)


        


    
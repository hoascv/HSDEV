from flask import Blueprint,render_template,flash, redirect, url_for, request, Response
from jinja2 import TemplateNotFound
from hswebapp import app,db
from hswebapp.models.models import TempLog,HumidityLog,PressureLog
import subprocess



views = Blueprint('views', __name__,template_folder='templates')

@app.before_first_request
def create_tables():
    db.create_all()

@views.route('/')
@views.route('/index')
def home():
    return render_template('pages/home.html')

@views.route('/addframe', methods=['GET','POST'])
def addframe1():
    form = FrameworkForm()
    if form.validate_on_submit():
        framework = form.framework.data
        description = form.description.data



        flash("Stored: ' framework {} and description {}'".format(framework,description))
        return redirect(url_for('home'))

    return render_template('add_framework.html',form=form)	

@views.route("/environment")
def temp():
    import sys
    import Adafruit_DHT
    import Adafruit_BMP.BMP085 as BMP085
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 23)
    values_sensor = BMP085.BMP085()

    try:
            query_result = db.engine.execute('select count(id) as num from templog')
            for row in query_result:
                result= row['num']
                            
            
            #templog = db.session.query(TempLog).all()
            templog= TempLog.query.order_by(TempLog.rdate.desc()).limit(10).all()
            humiditylog= HumidityLog.query.order_by(HumidityLog.rdate.desc()).limit(10).all()
            pressurelog= PressureLog.query.order_by(PressureLog.rdate.desc()).limit(10).all()
            
    except:
        flash("InvalidRequestError: {} ".format(sys.exc_info()[0]))
        raise
        db.session.rollback()
        return redirect(url_for('home'))
    finally:
        db.session.close()
        
        


    #db.session.close()
    
    if humidity is not None and temperature is not None and values_sensor is not None:
        return render_template("app_temp.html",ntemp=result,
                                temperature=temperature,temp = templog,
                                humidity=humidity,humididylog= humiditylog,
                                pressure=float(values_sensor.read_pressure()/100),
                                pressurelog=pressurelog
                                )
    else:
        return render_template("no_sensor.html")

@views.route('/readings', methods=["GET"])
def report_listreadings():

   # if request.method == "GET": 
    return render_template("readings.html", temperature = TempLog.query.order_by(TempLog.rdate.desc()).limit(50).all(), humidity = HumidityLog.query.order_by(HumidityLog.rdate.desc()).limit(50).all(), pressure = PressureLog.query.order_by(PressureLog.rdate.desc()).limit(50).all())   



@views.route('/grafics', methods=["GET"])
def report_grafics():
    import sys
    import Adafruit_DHT
    import Adafruit_BMP.BMP085 as BMP085
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 23)
    values_sensor = BMP085.BMP085()

    try:
            query_result = db.engine.execute('select count(id) as num from templog')
            for row in query_result:
                result= row['num']
                            
            
            #templog = db.session.query(TempLog).all()
            templog= TempLog.query.order_by(TempLog.rdate.desc()).limit(10).all()
            humiditylog= HumidityLog.query.order_by(HumidityLog.rdate.desc()).limit(10).all()
            pressurelog= PressureLog.query.order_by(PressureLog.rdate.desc()).limit(10).all()
            
    except:
        flash("InvalidRequestError: {} ".format(sys.exc_info()[0]))
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
                                pressurelog=pressurelog
                                )
    else:
        return render_template("no_sensor.html")
         
   
   
@views.route('/system', methods=["GET"])
def system():
    import psutil
    from hswebapp.models.hsutil import Hsutil
    return render_template("pages/system.html",psuvar=psutil,hsutil = Hsutil)    


    
@views.route('/shutdown',  methods=['GET'])
def shutdown():
    import subprocess
    
    #cmd = ["ls","-l"]
    cmd = ["shutdown"]
    
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    print ('Server shutdown')
    
    out,err = p.communicate()
    #return out
    return 'Server shutdown'
    
    
@views.route('/reboot',  methods=['GET'])
def reboot():
    
    
    #cmd = ["ls","-l"]
    cmd = ["reboot"]
    
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    print ('Server reboot')
    out,err = p.communicate()
    
    return out
    
def uptime():

    cmd = ["uptime"]
    
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    
    out,err = p.communicate()
    up = str(out)
    
    uptime = str(up.split(',')[0]).split('up')[-1]
    return uptime
    

@views.route('/system_uptime',  methods=['GET'])    
def system_uptime():
    
    return uptime()  
    
@views.route('/command',  methods=['GET'])  
def command():

    cmd = ["iwconfig"]
    
    p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    
    out,err = p.communicate()
    
    return out

    
    
    
    
    
    
    
@views.route('/about1', methods=["GET"])
def about1():
    return render_template("pages/about.html",varh='about')

@app.errorhandler(404)
def page_not_found(e):
    return render_template("errors/404.html"),404

@views.route('/register', methods=["GET"])
def register():
    return render_template("about.html",)

@views.route('/login', methods=["GET"])
def login():
    return render_template("about.html")

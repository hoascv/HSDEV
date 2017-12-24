from datetime import datetime
from hswebapp import db,model_saved,ma
from marshmallow import fields




#from flask_login import UserMixin 
#temperature_max_sensor1 = TempLog.query.order_by(TempLog.value.desc()).filter_by(sensorType='AM2302').first()
# create an abstract class 



#model_saved.connect(model_saved_signal, app)

class HumidityLog(db.Model):
    __tablename__ = 'humiditylog'
    id = db.Column(db.Integer, primary_key= True)
    sensor=db.Column(db.String(30))
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
   
    
    def __init__ (self,sensor,rdate,sensorLocation,sensorType,value):
        self.sensor=sensor
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def __repr__(self):
        return '<HumidityLog {}>'.format(self.sensorType)
    
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    
    @classmethod
    def get_max_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.value.desc()).first()
        
    @classmethod
    def get_min_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.value.asc()).first()
        
        
    def save_to_db(self):
        try: 
            db.session.add(self)
            db.session.commit()
            model_saved.send(self,message=self)     
        except:
            raise
            db.session.rollback()
        
        finally:
            pass

            
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
      
    def get_humidity(self):
        return str(self.value)+'%'
        
    def close_session(self):
        db.session.close()
    
    def get_id(self):
        return self.id
    
   
    def get_type(self):
        return type(self).__name__    
		
class TempLog(db.Model):
    __tablename__ = 'templog'
    id = db.Column(db.Integer, primary_key= True)
    sensor=db.Column(db.String(30)) 
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,sensor,rdate,sensorLocation,sensorType,value):
        self.sensor=sensor
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def __repr__(self):
        return '<TempLog {}>'.format(self.sensorType)
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    
    @classmethod
    def get_max_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.value.desc()).first()
    
    @classmethod
    def get_min_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.value.asc()).first()
    
    
    
    
    
    def save_to_db(self):
        try: 
            db.session.add(self)
            db.session.commit()
            model_saved.send(self,message=self)     
        except:
            raise
            db.session.rollback()
        
        finally:
            pass
        
    def close_session(self):
        db.session.close()    
        
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def close_session(self):
        db.session.close()
    
    def get_temperature(self):
        return str(self.value) +'C' 
        
    def get_type(self):
        return type(self).__name__    
    
    def get_id(self):
        return self.id
        
        
        
 
class TypeObject(fields.Field):
    def _serialize(self, obj):
        return type(obj)
        
 
  
class SensorLogSchema(ma.Schema):
    #class Meta:
        # Fields to expose
    #fields = ('value', 'sensorType', 'rdate') 
    sensor= fields.String()
    value = fields.Float()
    rdate  = fields.DateTime()
    sensorType = fields.String()
    type = TypeObject()    
    type_data = fields.Method("get_type_data")
   
    
    
    def get_type_data(self, obj):
        return type(obj).__name__
        
 

sensorlog_schema = SensorLogSchema()
sensorlogs_schema = SensorLogSchema(many=True) 

class PowerLogSchema(ma.Schema):
    
    sensor= fields.String()
    voltage = fields.Float()
    current = fields.Float()
    rdate  = fields.DateTime()
    sensorType = fields.String()
    type_data = fields.Method("get_type_data")

    def get_type_data(self, obj):
        return type(obj).__name__
        

powerlog_schema = PowerLogSchema()
powerlogs_schema =PowerLogSchema(many=True)


 
class PressureLog(db.Model):
    __tablename__ = 'pressurelog'
    id = db.Column(db.Integer, primary_key= True)
    sensor=db.Column(db.String(30))
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,sensor,rdate,sensorLocation,sensorType,value):
        self.sensor=sensor
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def __repr__(self):
        return '<PressureLog {}>'.format(self.sensorType)
        
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    
    @classmethod
    def get_max_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.value.desc()).first()
    
    @classmethod
    def get_min_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.value.asc()).first()
        
    
    def save_to_db(self):
        try: 
            db.session.add(self)
            db.session.commit()
            model_saved.send(self,message=self)     
        except:
            raise
            db.session.rollback()
        
        finally:
            pass
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def close_session(self):
        db.session.close()
        
    def get_value(self):
        return str(self.value)+'Pa'    
    
    def get_type(self):
        return type(self).__name__    

    def get_id(self):
        return self.id
        
        
        
class PowerLog(db.Model):
    __tablename__ = 'powerlog'
    id = db.Column(db.Integer, primary_key= True)
    sensor=db.Column(db.String(30))
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    voltage  = db.Column(db.Float(precision=2))
    current =  db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,sensor,rdate,sensorLocation,sensorType,voltage,current):
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.voltage=voltage
        self.current = current
        self.sensor=sensor
    
    def __repr__(self):
        return '<PowerLog {}>'.format(self.sensorType)
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'voltage':self.voltage,'current':self.current,'sensorType':self.sensorType}

    @classmethod
    def get_max_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.voltage.desc()).first()
    
    @classmethod
    def get_min_value(cls,sensorType):
        return cls.query.filter_by(sensorType=sensorType).order_by(cls.voltage.asc()).first()
    
    
    def save_to_db(self):
        try: 
            db.session.add(self)
            db.session.commit()
            model_saved.send(self,message=self)     
        except:
            raise
            db.session.rollback()
        
        finally:
            pass
        
    def close_session(self):
        db.session.close()    
        
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def close_session(self):
        db.session.close()
    
    def get_voltage(self):
        return str(self.voltage)

    def get_current(self):
        return str(self.current)
    
    def get_type(self):
        return type(self).__name__    
    
    def get_id(self):
        return self.id
        

    
#class User(UserMixin,db.Model):
#    id = db.Column(db.Integer,primary_key=True)
#    username= db.Column(db.String(15), unique=True)
#    email= db.Column(db.String(50), unique=True)
#    password =db.Column(db.String(80))

    
    
    
		
#db.create_all()
class EventLog(db.Model):
    id          = db.Column(db.Integer, primary_key= True)
    ob_id       = db.Column(db.Integer)
    date_added  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ob_type     = db.Column(db.String(30))
    obs         = db.Column(db.String(50))
 
    def save_to_db(self):
        try: 
            db.session.add(self)
            db.session.commit()
                
        except:
            raise
            db.session.rollback()
        
        finally:
            pass 
            
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()        
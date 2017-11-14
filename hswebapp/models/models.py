from datetime import datetime
from hswebapp import db
 

class HumidityLog(db.Model):
    __tablename__ = 'humiditylog'
    id = db.Column(db.Integer, primary_key= True)
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,rdate,sensorLocation,sensorType,value):
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    @classmethod
    def find_by_sensorLocation(cls,sensorLocation):
        return cls.query.filter_by(sensorLocation=sensorLocation)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def get_date(self):
        return rdate    
        
    def close_session(self):
        db.session.close()
    def get_value(self):
        return  str(self.value) +"%"
		
class TempLog(db.Model):
    __tablename__ = 'templog'
    id = db.Column(db.Integer, primary_key= True)
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,rdate,sensorLocation,sensorType,value):
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    @classmethod
    def find_by_sensorLocation(cls,sensorLocation):
        return cls.query.filter_by(sensorLocation=sensorLocation)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def close_session(self):
        db.session.close()    
        
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def close_session(self):
        db.session.close()
    
    def get_value(self):
        return str(self.value)
 
 
class PressureLog(db.Model):
    __tablename__ = 'pressureLog'
    id = db.Column(db.Integer, primary_key= True)
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    value  = db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,rdate,sensorLocation,sensorType,value):
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.value=value
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'value':self.value,'sensorType':self.sensorType}

    @classmethod
    def find_by_sensorLocation(cls,sensorLocation):
        return cls.query.filter_by(sensorLocation=sensorLocation)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
	
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
        
    def close_session(self):
        db.session.close()

class PowerLog(db.Model):
    __tablename__ = 'powerlog'
    id = db.Column(db.Integer, primary_key= True)
    rdate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sensorLocation = db.Column(db.String(15))
    voltage  = db.Column(db.Float(precision=2))
    current =  db.Column(db.Float(precision=2))
    sensorType = db.Column(db.String(15))
    
    def __init__ (self,rdate,sensorLocation,sensorType,voltage,current):
        self.rdate = rdate
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
        self.voltage=voltage
        self.current = current
    
    def json(self):
        return {'data':self.data,'sensorLocation':self.sensorLocation,'voltage':self.voltage,'current':self.current,'sensorType':self.sensorType}

    @classmethod
    def find_by_sensorLocation(cls,sensorLocation):
        return cls.query.filter_by(sensorLocation=sensorLocation)
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
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
            
	
		
#db.create_all()

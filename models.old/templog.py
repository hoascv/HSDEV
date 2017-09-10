from hswebapp import db

class TempLog(db.Model):
    __tablename__ = 'templog'

    id     = 		db.Column(db.Integer, primary_key= True)
    data   = 		db.Column(db.Date)
    sensorLocation =	db.Column(db.String(5))
    value  = 		db.Column(db.Float(precision=2))
    sensorType = 	db.Column(db.String(10))
    
    def __init__(self,data,sensorLocation,sensorType):
        self.data = data
        self.sensorLocation = sensorLocation
        self.sensorType = sensorType
    
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

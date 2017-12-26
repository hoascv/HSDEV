from datetime import datetime
from hswebapp import db,model_saved,ma
from hswebapp.models.models import TempLog,PowerLog,PressureLog,HumidityLog 
from marshmallow import fields


 
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


 

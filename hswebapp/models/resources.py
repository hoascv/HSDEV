from datetime import datetime
from hswebapp import db,model_saved,ma
from hswebapp.models.sensor_models import TempLog,PowerLog,PressureLog,HumidityLog 
from marshmallow import fields
from flask import  url_for,jsonify

 
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

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
                'items': [item.to_dict() for item in resources.items],
                '_meta': {
                    'page': page,
                    'per_page': per_page,
                    'total_pages': resources.pages,
                    'total_items': resources.total
                 },
                '_links': {
                    'self': 'https://hswebapp.com' +  url_for(endpoint, page=page, per_page=per_page,**kwargs),
                    'next': 'https://hswebapp.com' + url_for(endpoint, page=page + 1, per_page=per_page,**kwargs) if resources.has_next else None,
                    'prev': 'https://hswebapp.com' + url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
                 }
               }
        return data



 

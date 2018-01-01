from flask_restful import Resource, reqparse
from flask import Blueprint, request, Response,jsonify

from hswebapp import app,db

from hswebapp.api import apiv0
from datetime import datetime
from time import sleep

from werkzeug.security import generate_password_hash,check_password_hash
from hswebapp.models.system_models import User,Logs
from hswebapp.models.sensor_models import TempLog,HumidityLog,PressureLog,PowerLog,EventLog
from hswebapp.models.resources import sensorlogs_schema,powerlogs_schema

import copy


@apiv0.route('/apiv1/templogs/<int:lastreadings>', methods=['GET'])
def get_templogs(lastreadings,):

    templog= TempLog.query.order_by(TempLog.rdate.desc()).limit(lastreadings).all()
    result = sensorlogs_schema.dump(templog)
    return jsonify({'templogs': result.data})

@apiv0.route('/apiv1/sensorlog', methods=['GET'])
def get_sensorlogs():
    
    page = request.args.get('page', 1, type=int)
    #sensor = request.args.get('sensor', 'temperature_sensor1',type=string)
     
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    #example:
    #data = User.to_collection_dict(User.query, page, per_page, 'apiv0.get_users')
    return jsonify(data)

    
    
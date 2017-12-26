from flask_restful import Resource, reqparse
from flask import Blueprint, request, Response,jsonify

from hswebapp import app,db

from hswebapp.api import apiv0
from datetime import datetime
from time import sleep

from werkzeug.security import generate_password_hash,check_password_hash
from hswebapp.models.system_models import User,Logs
from hswebapp.models.models import TempLog,HumidityLog,PressureLog,PowerLog,EventLog
from hswebapp.models.resources import sensorlogs_schema,powerlogs_schema

import copy


@apiv0.route('/templogs/<int:lastreadings>', methods=['GET'])
def get_templogs(lastreadings,):

    templog= TempLog.query.order_by(TempLog.rdate.desc()).limit(lastreadings).all()
    result = sensorlogs_schema.dump(templog)
    return jsonify({'templogs': result.data})
    
    
    #return sensorlogs_schema.jsonify(templog)
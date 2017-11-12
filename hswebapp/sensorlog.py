import os,sys 
from datetime import datetime 
import sys; sys.path.append('/var/www/hswebapp')
import  I2C_LCD_driver
from time import *
import Adafruit_DHT 
import Adafruit_BMP.BMP085 as BMP085
from hswebapp.models.models import TempLog,HumidityLog,PressureLog,PowerLog
from time import sleep

import serial
import ast

values_sensor = BMP085.BMP085()
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 23) 

if humidity is not None and temperature is not None:
    reading = TempLog(datetime.now(),'livingroom','AM2302',temperature)
    reading.save_to_db()
    readingH= HumidityLog(datetime.now(),'livingroom','AM2302',humidity)
    readingH.save_to_db()
  #  readingH.close_session()

if values_sensor is not None:
    temp_reading= TempLog(datetime.now(),'livingroom','BMP180',values_sensor.read_temperature())
    temp_reading.save_to_db()
  #  temp_reading.close_session()
    
    pressure_reading=PressureLog(datetime.now(),'livingroom','BMP180',values_sensor.read_pressure())
    pressure_reading.save_to_db()
  #  pressure_reading.close_session()

mylcd = I2C_LCD_driver.lcd() 
mylcd.backlight(1)    
mylcd.lcd_display_string("Temp:" + temp_reading.get_value()+ " / " +reading.get_value() ,1,0)

mylcd.lcd_display_string("Hum:" + readingH.get_value(),2,0)
# check if people is around


  
  
ser = serial.Serial ("/dev/ttyS0",timeout=4)    #Open named port 
ser.baudrate = 57600                     #Set baud rate to 57600

ser.write(b'0')
print("Waiting: {}".format(ser.in_waiting))
raw = str(ser.readline(),'utf-8')
     
line = raw.replace("\r\n","")
print("Received: {}".format(line))

try :
    data =ast.literal_eval(line)
except :
    data = {'STATUS':'UNABLE TO GET DATA FROM THE DEVICE SENSOR'}
    
        
  
#{'DEVICE_ID':'DS1','HEADER':'register','STATUS':'REGISTERED'}
if (data['STATUS']=='REGISTERED'):
    ser.write(b'7')
#{'DEVICE_ID':'DS1','HEADER':'data','STATUS':'Sucess','SENSOR_TYPE':'Voltage','SENSOR_VALUE':4.84}
    print("Waiting: {}".format(ser.in_waiting))
    raw = str(ser.readline(),'utf-8')    
    line = raw.replace("\r\n","")
    print("Received: {}".format(line))
    data =ast.literal_eval(line)
    power_reading = PowerLog(datetime.now(),'remote','SolarCell',float(data['SENSOR_VALUE']),0)
    power_reading.save_to_db()
    
else:
    print("NOT CONNECTION")
    print(data['STATUS'])
    
ser.close()    


sleep(60)
mylcd.backlight(0)



	
#print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
#print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
#print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
#print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

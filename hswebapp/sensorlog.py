import os,sys 
from datetime import datetime 
import sys; sys.path.append('/var/www/hswebapp')
import  I2C_LCD_driver
from time import *
import Adafruit_DHT 
import Adafruit_BMP.BMP085 as BMP085
from hswebapp.models.models import TempLog,HumidityLog,PressureLog,PowerLog
from hswebapp import app
from time import sleep
import serial
import ast




def response():

    try:
        app.logger.info("Waiting: {}".format(ser.in_waiting))
        raw = str(ser.readline(),'utf-8')    
        line = raw.replace("\r\n","")
        app.logger.info("Received: {}".format(line))
        data = ast.literal_eval(line)
        
    except:
         app.logger.error('UNABLE TO GET DATA FROM THE DEVICE SENSOR: {}'.format(datetime.now()))
         data={'STATUS':'UNABLE TO GET DATA FROM THE DEVICE SENSOR'}
    
    return data




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
sleep(2)
data = response()
        
  
#{'DEVICE_ID':'DS1','HEADER':'register','STATUS':'REGISTERED'}
if (data['STATUS']=='REGISTERED'):
    ser.write(b'7') # Retrieve remote power
    sleep(2)
#{'DEVICE_ID':'DS1','HEADER':'data','STATUS':'Sucess','SENSOR_TYPE':'Voltage','SENSOR_VALUE':4.84}
    
    data = response()
    
    power_reading = PowerLog(datetime.now(),'Remote','SolarCell',float(data['SENSOR_VALUE']),0)
    power_reading.save_to_db()
    
    ser.write(b'2')
    sleep(2)
    data = response()
    reading = TempLog(datetime.now(),'Remote','DH11',data['SENSOR_VALUE'])
    reading.save_to_db()
    
    ser.write(b'4')
    sleep(2)
    data = response()
    reading = HumidityLog(datetime.now(),'Remote','DH11',data['SENSOR_VALUE'])
    reading.save_to_db()
    
      
    
    
else:
    app.logger.info((data['STATUS']))
    
ser.close()    




#app.logger.warning('A warning occurred (%d apples)', 42)
#app.logger.error('An error occurred')
#app.logger.info('Info')



def response ():   
    pass
    
    #except :
     #   app.logger.error('UNABLE TO GET DATA FROM THE DEVICE SENSOR: {}'.format(datetime.now()))
	
    
#sleep(60)
mylcd.backlight(0)

    
#print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
#print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
#print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
#print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

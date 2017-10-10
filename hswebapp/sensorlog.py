import os,sys 
from datetime import datetime 
import sys; sys.path.append('/var/www/hswebapp')
import  I2C_LCD_driver
from time import *

mylcd = I2C_LCD_driver.lcd()






import Adafruit_DHT 
import Adafruit_BMP.BMP085 as BMP085
from hswebapp.models.models import TempLog,HumidityLog,PressureLog


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
    
    
mylcd.lcd_display_string("Temp:" + temp_reading.get_value()+ " / " +reading.get_value() ,1,0)

mylcd.lcd_display_string("Hum:" + readingH.get_value(),2,0)

	
#print('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
#print('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
#print('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
#print('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

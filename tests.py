import serial
#defining the RPi's pins as Input / Output
import RPi.GPIO as GPIO

#importing the library for delaying command.
import time 
import ast


#used for GPIO numbering
GPIO.setmode(GPIO.BCM) 

#closing the warnings when you are compiling the code
GPIO.setwarnings(False) 

cmdPin = 18 

GPIO.setup(cmdPin,GPIO.HIGH)

count=10
ser = serial.Serial ("/dev/ttyS0",timeout=4)    #Open named port 
ser.baudrate = 57600                     #Set baud rate to 57600

# check the device sensors                 
ser.write(b'0')


print("Waiting: {}".format(ser.in_waiting))

raw = str(ser.readline(),'utf-8')
     
line = raw.replace("\r\n","")
print("Received: {}".format(line))

data =ast.literal_eval(line)

#handle the data

ser.write(b'1')
raw = str(ser.readline(),'utf-8')
data =ast.literal_eval(line)    
line = raw.replace("\r\n","")
print("Received: {}".format(line))

ser.write(b'2')
raw = str(ser.readline(),'utf-8')    
line = raw.replace("\r\n","")
print("Received: {}".format(line))
data =ast.literal_eval(line)

ser.write(b'3')
raw = str(ser.readline(),'utf-8')    
line = raw.replace("\r\n","")
print("Received: {}".format(line))
data =ast.literal_eval(line)


ser.write(b'4')
raw = str(ser.readline(),'utf-8')    
line = raw.replace("\r\n","")
print("Received: {}".format(line))
data =ast.literal_eval(line)


ser.write(b'5')
raw = str(ser.readline(),'utf-8')    
line = raw.replace("\r\n","")
print("Received: {}".format(line))
data =ast.literal_eval(line)



ser.write(b'6')
raw = str(ser.readline(),'utf-8')    
line = raw.replace("\r\n","")
print("Received: {}".format(line))
data =ast.literal_eval(line)


ser.write(b'7')
raw = str(ser.readline(),'utf-8')    
line = raw.replace("\r\n","")
print("Received: {}".format(line))
data =ast.literal_eval(line)



ser.close()

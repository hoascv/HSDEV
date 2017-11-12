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
ser = serial.Serial ("/dev/ttyS0",timeout=2)    #Open named port 
ser.baudrate = 57600                     #Set baud rate to 9600
ser.write(b'inicio transm')

time.sleep(1)

while (count> 0):
       
    data =b'teste'                     #Read ten characters from serial port to data
    ser.write(b'TH1\n')
    ser.write(b'TH1\n')    #Send back the received data
    ser.write(b'TH1\n')
    ser.write(b'TH1\n')
    ser.write(b'TH1\n')
   # ser.write(count)
    print("Waiting: {}".format(ser.in_waiting))
    line = str(ser.readline(),'utf-8')
    raw = line.replace("\r\n","")
    print("Received: {}".format(raw))
    count-=1


ser.close()

reading =ast.literal_eval(raw)
print ("result:{}".format(reading[1]))


GPIO.setup(cmdPin,GPIO.LOW)
print("low")
time.sleep(1)
print("low wait 20")

ser1 = serial.Serial ("/dev/ttyS0",timeout=1)
ser1.baudrate = 9600
print(ser1.stopbits)
print(ser1.parity)
time.sleep(1)
ser1.write(b'AT+RX')
time.sleep(2)
print(ser1.in_waiting)
print(ser1.read(4))
GPIO.setup(cmdPin,GPIO.HIGH)
ser1.close()





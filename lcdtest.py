import  I2C_LCD_driver
import time
import socket
import fcntl
import struct
import datetime

mylcd = I2C_LCD_driver.lcd()
time =str(datetime.datetime.now())

mylcd.lcd_display_string(time,2,0)


#while True:
#    mylcd.lcd_display_string("Hello world!",2,0)
# mylcd.lcd_display_string("Hello world!",2,0)
#    time.sleep(1)
#    mylcd.lcd_clear()
#    time.sleep(1)

#def get_ip_address(ifname):
#    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#    return socket.inet_ntoa(fcntl.ioctl(
#        s.fileno(),
#        0x8915, 
#        struct.pack('256s', ifname[:15])
#    )[20:24])

#mylcd.lcd_display_string("IP Address:", 1) 

#mylcd.lcd_display_string(get_ip_address('eth0'),2,0)

#str_pad = " " * 16
#my_long_string = str(datetime.datetime.now())
#my_long_string = str_pad + my_long_string

#while True:
#    for i in range (0, len(my_long_string)):
#        lcd_text = my_long_string[i:(i+16)]
#        mylcd.lcd_display_string(lcd_text,1)
#        time.sleep(0.4)
#        mylcd.lcd_display_string(str_pad,1)
        

import subprocess
import psutil

class Hsutil:
    def __init__(self,name):
        self.name=name
        
    @classmethod	
    def getUptime(cls):   
    #'15:53:51 up 2:16, 1 user, load average: 0.03, 0.03, 0.05'
    #'16:48:37 up 1 min, 0 users, load average: 0.23, 0.05, 0.02'
        raw=cls.procommand(cmdstring="uptime")
        uptime = str(raw.split(',')[0]).split('up')[-1]
        return uptime
        
    @classmethod
    def procommand(cls,cmdstring):
        cmd = [cmdstring]
        p = subprocess.Popen(cmd, stdout = subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE)
    
        out,err = p.communicate()
        return str(out)
        
        
    @classmethod
    def getSSID(cls):
        raw=cls.procommand(cmdstring="iwconfig")
        ssid= raw [raw.find('"')+1:raw.find('"',raw.find('"')+1, len(raw))]
        lq = raw[(raw.find('Link Quality=')+len('Link Quality=')):((raw.find('Link Quality=')+len('Link Quality'))+6)]
        return {'ssid':ssid,'Link_Quality':lq}
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
    
    @classmethod
    def get_remaining_time(cls,timedelta):
        remaining_time=''
        days=timedelta.days
        hours=int(timedelta.seconds/3600)
        minutes = int((timedelta.seconds%3600)/60)
        seconds = int( (timedelta.seconds)%60)
        
        if days < 0 :    
            return 'Expired'    
            
        elif  days > 0 :
            return ' {} Days {} Hours  {} Minutes {} and seconds'.format(days,hours,minutes,seconds)
        elif days == 0 and hours > 0 :
            return ' {} Hours  {} Minutes {} and seconds'.format(hours,minutes,seconds)
        
        elif days == 0 and hours == 0 and minutes > 0:
            return ' {} Minutes {} and seconds'.format(minutes,seconds)
            
        else :
            return '{} seconds'.format(seconds)
        
        
        
        return remaining_time
        
            

            
    
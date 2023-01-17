import struct 
import datetime
class NtpTime: 
    NTPEPOCH = datetime.datetime(1900, 1, 1, 0, 0, 0)
    UNIXEPOCH = datetime.datetime(1970, 1, 1, 0, 0, 0)
    def fromRaw(raw:int  ):
        ''' ctor that gets raw data of NTP date format in int '''
        raw =raw.to_bytes(8,"big")
        fraction ,secs  = struct.unpack('!II',raw )
        print(secs)
        print(fraction)
        return NtpTime(secs,fraction)
        
    def __init__(self,secs , fraction): 
        '''set NTP_Time from secs and fraction '''
        self.fraction = fraction
        self.secs = secs 
        
    def __bytes__(self) : 
        ''' converts the value to bytes '''
        return struct.pack("!II", self.fraction , self.secs)
    
    def __int__(self): 
        '''converts the value to int  '''
        return self.secs 
    
    def __float__(self): 
        '''converts the value to float  '''
        return self.secs + self.fraction * 10 ** -(len(str(self.fraction))) 
    
    def __repr__(self) : 
        ''' printing method '''
        return f"""secs : {self.secs} , fraction : {self.fraction} """
    
    def convertUnixTONtpDate(EpochTime:int):
       ''' gets UNIX epoch (can be get by time.time())  and  converts it to NTP EPOCH '''
       diffUnixAndNtp =  datetime.datetime.fromtimestamp(EpochTime) - NtpTime.NTPEPOCH
       secs = diffUnixAndNtp.days*24*60*60+diffUnixAndNtp.seconds
       milisecs = diffUnixAndNtp.microseconds
       return NtpTime(secs , milisecs)

        
  
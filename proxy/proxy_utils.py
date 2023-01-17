
import os 
import enum
from urlspoof.spoofer import despoof_url
from urlspoof.ending import URLAdds
import datetime
class Way(enum.Enum):
    From = 0 
    To = 1
def cleanHeaders(headers : dict , way :Way  )->dict: 
    ''' cleans the headers from unwanted headers '''
    
    
    ALLOWED_HEADERS = {"cookie","user-agent",
                       "x-csrf-token","content-type",
                       "accept","accept-language",
                       "accept-encoding","server",""}
    res = {}
    try : 
        for key , value  in headers.items() : 
            if key.lower() in ALLOWED_HEADERS : 
                res[key]=value
            if key.lower() == "date": 
                res[key] = (datetime.datetime.now() +datetime.timedelta(hours= 24 * (365 * 3+1)  ) ).strftime(' %A, %-d %b %Y %X GMT')
    except Exception as e :
        print(f"clean function error {e}")
    return res


def cleanHostName(hostName : str )->str: 
    ''' cleans the spoofed url and returns a valid https orignal hostname '''
    return despoof_url(hostName)



import requests
import datetime
def getHstsHeader(siteName): 
    ''' get the max age of website '''
    hsts = None
    try :
        respone = requests.get(siteName,timeout=10)
        hsts = respone.headers.get("Strict-Transport-Security")
        if not hsts :
            raise Exception("")
        hsts = hsts.split(";")
        if not hsts : 
            return [datetime.timedelta(seconds= 0) , "no","no"]
        if hsts and "max-age" in hsts[0] and "=" in hsts[0] and hsts[0].split("=")[1].isdigit(): 
                hsts[0] =datetime.timedelta(seconds= int(hsts[0].split("=")[1]))
        else : 
            hsts.insert(0,datetime.timedelta(seconds= 0) )
    except  : 
      ...
        
    if not hsts or isinstance(hsts[0],str) : 
        return [datetime.timedelta(seconds= 0) , "no","no"]
    return hsts



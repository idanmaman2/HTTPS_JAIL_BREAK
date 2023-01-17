
import gzip
import os 
import io 
import enum
class Way(enum.Enum):
    From = 0 
    To = 1
def cleanHeaders(headers : dict , way :Way  )->dict: 
    ''' cleans the headers from unwanted headers '''
    def parserTo(value):
        return value.replace("http","https")
    def parserFrom(value):
         return value.replace("https","http")
    
    ALLOWED_HEADERS = {"cookie","user-agent","referer",
                       "x-csrf-token","content-type",
                       "host","accept","accept-language",
                       "accept-encoding","connection","access-control-allow-origin"}
    res = {}
    methods = {Way.To  : parserTo , Way.From : parserFrom } 
    try : 
        for key , value  in headers.items() : 
            if key.lower() in ALLOWED_HEADERS : 
                res[key]=methods[way](value)
    except Exception as e :
        print(f"clean function error {e}")
    return res


def cleanHostName(hostName : str )->str: 
    ''' cleans the spoofed url and returns a valid https orignal hostname '''
    cleaned = hostName.removeprefix("http://")
    return f"https://{cleaned}/"




def saveContent(content , contentName , path,typeName ):
    os.makedirs(f"{path}/out/f{typeName}/" , exist_ok=True) 
    with open(f"{path}/out/{typeName}/{contentName.replace('/','_') if contentName else 'empty'}" , 'wb') as file : 
        file.write(content) 
        



def cleanCookies(cookies:str): 
    ''' cleans the DOMAIN cookie to the new url...'''
    ...


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
        return value.replace("http","https").replace("vvvvvv","www")
    def parserFrom(value):
         return value.replace("http","https").replace("vvvvvv","www")
    
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
    cleaned = hostName.removeprefix("http://").removeprefix("vvvvvv.")
    return f"https://www.{cleaned}/"

def saveImage(imageContent , imageName , path ):
    os.makedirs(path , exist_ok=True) 
    with open(f"{path}/images/{path.replace('/','_') if path else 'empty'}" , 'wb') as file : 
        file.write(imageContent) 
def saveVideo(VideoContent , videoName , path ):
    """ each http packet with the header `video/mp4` is aved with that function into the local computer """
    os.makedirs(path , exist_ok=True) 
    with open(f"{path}/videos/{path.replace('/','_') if path else 'empty'}" , 'wb') as file : 
        file.write(VideoContent) 


def cleanCookies(cookies:str): 
    ''' cleans the DOMAIN cookie to the new url...'''
    ...

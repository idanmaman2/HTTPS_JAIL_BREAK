
import gzip
import os 
import io 
def cleanHeaders(headers : dict  )->dict: 
    ''' cleans the headers from unwanted headers '''
    ALLOWED_HEADERS = {"cookie","user-Agent","referer","x-csrf-token","content-type"}
    res = {} 
    for key , value  in headers.items() : 
        if key.lower() in ALLOWED_HEADERS : 
            res[key]=value
    return res


def cleanHostName(hostName : str )->str: 
    ''' cleans the spoofed url and returns a valid https orignal hostname '''
    cleaned = hostName.removeprefix("http://").removeprefix("vvvvvv.")
    return f"https://www.{cleaned}/"

def saveImage(imageContent , imageName , path ):
    os.makedirs(path , exist_ok=True) 
    with open(f"{path}/images/{path.replace('/','_') if path else 'empty'}" , 'wb') as file : 
        file.write(imageContent) 


def unCompressRespone(respone:bytes) -> bytes :
    return  gzip.open(io.StringIO(respone)).read()

def cleanCookies(cookies:str): 
    ''' cleans the DOMAIN cookie to the new url...'''
    ...

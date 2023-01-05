
import gzip
import os 

def cleanHeaders(headers : dict  )->dict: 
    ''' cleans the headers from unwanted headers '''
    BLACK_LIST = {"content-encoding", "content-length", "transfer-encoding", "connection"} 
    cleanedHeaders = { }
    for key in headers : 
        if key.lower() not in headers: 
            cleanedHeaders[key] = headers[key]
    return cleanedHeaders

def cleanHostName(hostName : str )->str: 
    ''' cleans the spoofed url and returns a valid https orignal hostname '''
    cleaned = hostName.removeprefix("http://").startswith("vvvvvv.")
    return f"https://www.{cleaned}/"

def saveImage(imageContent , imageName , path ):
    os.makedirs(path , exist_ok=True) 
    with open(f"{path}/images/{path.replace('/','_') if path else 'empty'}" , 'wb') as file : 
        file.write(respone.content) 


def unCompressRespone(respone:bytes) -> bytes :
    return  gzip.decompress(respone)

def cleanCookies(cookies:str): 
    ...

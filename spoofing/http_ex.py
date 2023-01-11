import re 
class HTTP : 
    HTTPSEPERATE = "\r\n"
    HTTPEND = "\r\n\r\n"
    
    def __init__(self,version : str ,headers : list ,content : bytes )->None : 
        ''' ctor '''
        versionSplitted = version.split(" ")
        self.version = {
            "version": versionSplitted[0],
            "code":versionSplitted[1],
            "code_name":versionSplitted[2]
        }
        self.headers =dict([(header[:header.find(":")], header[header.find(":")+1:]) for header in headers])
        self.content = content  
        
    def fromRawPack(raw:bytes):
        ''' get raw content of http packet and create HTTP object ''' 
        try : 
            rawEnd = raw.index(bytes(HTTP.HTTPEND,encoding="ascii")) #exit to the catch if it cant find the needle in the histack 
            data = raw[:rawEnd].decode(encoding="ascii").split(HTTP.HTTPSEPERATE)
            return HTTP(data[0],data[1:] ,raw[rawEnd + len(HTTP.HTTPEND):])        
        except Exception as e : 
            return None 
        
    def toRaw(self)->bytes: 
        ''' return the HTTP object to raw data '''
        return bytes( HTTP.HTTPSEPERATE.join([" ".join(self.version.values())]+[ ":".join(header) for header in  self.headers.items() ])+HTTP.HTTPEND ,encoding="ascii" ) + self.content
    

    
    def __repr__(self) -> str:
        '''printing '''
        return f"""
                good : { self.version["code"] == "301" } 
                version : {self.version}
                headers : {self.headers}
                content : {self.content}
                """
                
    def sslStripavailable(self)->bool:
        ''' check if sslstriping can be preformed'''
        return  re.match("30[0-8]",self.version["code"]) and "Location" in self.headers

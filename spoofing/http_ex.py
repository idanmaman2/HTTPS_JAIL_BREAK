import re 
import datetime
import time
import gzip 
class HTTP : 
    HTTPSEPERATE = "\r\n"
    HTTPEND = "\r\n\r\n"
    def __init__(self,version : str ,headers : list ,content : bytes ,ip :str)->None : 
        ''' ctor '''
        versionSplitted = version.split(" ")
        self.version = {
            "version": versionSplitted[0],
            "code":versionSplitted[1],
            "code_name":versionSplitted[2]
        }
        self.ip = ip 
        self.headers =dict([(header[:header.find(":")], header[header.find(":")+1:]) for header in headers])
        self.content = content  
        
    def fromRawPack(raw:bytes, ip :str ):
        ''' get raw content of http packet and create HTTP object ''' 
        try : 
            rawEnd = raw.index(bytes(HTTP.HTTPEND,encoding="ascii")) #exit to the catch if it cant find the needle in the histack 
            data = raw[:rawEnd].decode(encoding="ascii").split(HTTP.HTTPSEPERATE)
            return HTTP(data[0],data[1:] ,raw[rawEnd + len(HTTP.HTTPEND):],ip)        
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
    def chunkedContent(self)->list:
        chunks = []
        data = self.content
        while(chunks != ''):
            offset = data.find(bytes(HTTP.HTTPSEPERATE,encoding="ascii"))
            if offset == -1 : 
                break 
            else : 
                chunks.append(data[:offset])
                data = data[offset+len(HTTP.HTTPSEPERATE) : ]
        return chunks
    
    
    def getFakeTIme():
        return (datetime.datetime.now() +datetime.timedelta(hours= 24 * (365 * 3+1)  ) ).strftime(' %A, %-d %b %Y %X GMT')

    def timeTravel(self): 
        if "Date" in self.headers : 
            self.headers["Date"]=HTTP.getFakeTIme()
            
    def chromeKillerAvailable(self)->bool : 
        return "Content-Disposition" in self.headers and self.headers["Content-Disposition"] == ' attachment; filename="json.txt"; filename*=UTF-8\'\'json.txt' 
    
    def sslStripavailable(self)->bool:
        ''' check if sslstriping can be preformed
        '''
        return  re.match("30[0-8]",self.version["code"]) and "Location" in self.headers


"""
Example for Raw HTTP : 
    b'HTTP/1.1 200 OK\r\n
    Date: Wed, 28 Dec 2022 21:08:24 GMT\r\n
    Server: Apache\r\nLast-Modified: Fri, 17 Sep 2021 19:26:14 GMT\r\n
    Accept-Ranges: bytes\r\n
    Vary: Accept-Encoding,User-Agent\r\n
    Content-Encoding: gzip\r\n
    Content-Length: 12038\r\n
    Keep-Alive: timeout=15, max=95\r\n
    Connection: Keep-Alive\r\nContent-Type: text/html\r\n
    Set-Cookie: BIGipServer~CUIT~www.columbia.edu-80-pool=1764244352.20480.0000; expires=Thu, 29-Dec-2022 03:08:24 GMT; path=/; Httponly\r\n\r\n'

"""



class HTTP : 
    HTTPSEPERATE = "\r\n"
    HTTPEND = "\r\n\r\n"
    
    def __init__(self,version : str ,headers : list ,content : bytes )->None : 
        versionSplitted = version.split(" ")
        self.version = {
            "version": versionSplitted[0],
            "code":versionSplitted[1],
            "code_name":versionSplitted[2]
        }
        self.headers =dict([(header[:header.find(":")], header[header.find(":")+1:]) for header in headers])
        self.content = content  
        
    def FromRawPack(raw:bytes): 
        try : 
            rawEnd = raw.index(bytes(HTTP.HTTPEND,encoding="ascii")) #exit to the catch if it cant find the needle in the histack 
            data = raw[:rawEnd].decode(encoding="ascii").split(HTTP.HTTPSEPERATE)
            return HTTP(data[0],data[1:] ,raw[rawEnd + len(HTTP.HTTPEND):])        
        except Exception as e : 
            return None 
        
    def toRaw(self)->bytes: 
        return bytes( HTTP.HTTPSEPERATE.join([" ".join(self.version.values())]+[ ":".join(header) for header in  self.headers.items() ])+HTTP.HTTPEND ,encoding="ascii" ) + self.content
    
    def __repr__(self) -> str:
        return f"""
                good : { self.version["code"] == "301" } 
                valid : {self.version}
                headers : 
                        {self.headers}
                content : {self.content}
                """
                
    def sslStripavailable(self)->bool:
        return  self.version["code"] == "301" and "Location" in self.headers

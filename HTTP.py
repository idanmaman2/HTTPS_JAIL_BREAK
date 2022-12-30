
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
from enum import Enum


class HTTPType(Enum):
    Header =1 
    TOK_END = 2 
    TOK_COMMA = 3 

class HTTP : 
    def __init__(self,version,headers): 
        versionSplitted = version.split(" ")
        self.version = {
            "version": versionSplitted[0],
            "code":versionSplitted[1],
            "code_name":versionSplitted[2]
        }
        self.headers =dict([(header[:header.find(":")], header[header.find(":")+1:]) for header in headers])
    def FromRawPack(raw:bytes): 
        try : 
            last_token ="" 
            last_content =""
            token_type = None 
            data = []
            print("decoding...")
            for bit in raw: 
                bitStr =chr(bit)
                match(bitStr):
                    case '\n': 
                        if last_token == '\r': 
                            data.append(last_content)
                            last_token +='\n' 
                            last_content=""
                        elif last_token == '\r\n\r': 
                            return HTTP(data[0],data[1:])
                        else : 
                            last_content+='\n'
                    case '\r': 
                        last_token = '\r' if last_token != '\r\n' else  '\r\n\r'
                    case other : 
                        last_token=""
                        last_content+=bitStr
                
        except Exception as e : 
            print(e)
            return None 
    def toRaw(self): 
        return bytes( "\r\n".join([" ".join(self.version.values())]+[ ":".join(header) for header in  self.headers.items() ])+"\r\n\r\n" ,encoding="ascii" )
    def __repr__(self) -> str:
        return f"""
                good : { self.version["code"] == "301" } 
                valid : {self.version}
                headers : 
                        {self.headers}
                """
    def sslStripavailable(self):
        if self.version["code"] == "301": 
            location = self.headers.get("Location")
            if location : 
                return True 
        return False 
                

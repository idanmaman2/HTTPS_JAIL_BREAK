
from spoofing.objects.http_ex import HTTP 
import re 
    
def spoofedURL(url:str)->str: 
    '''spoofing the url for sslstrip and replacing www with vvvvvvv and changing https to http and erase port specify '''
    spoofed = url.strip().removeprefix('https://').removeprefix("http://")
    ending = "vvvvvv."
    if spoofed.startswith("www."): 
        spoofed = spoofed.removeprefix('www.').strip()
        ending = "vvvvv."
    portSpecify = re.search(":\d+",spoofed)
    if portSpecify : 
        spoofed = spoofed[:portSpecify.start()] 
    return f"http://{ending}{spoofed}" 
def http_spoof(httpPack:HTTP):
    httpPack.headers["Location"]=spoofedURL(httpPack.headers["Location"])
    return httpPack
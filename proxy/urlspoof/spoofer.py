
import urlspoof.ending as ending
def spoof_url(url:str)->str:
    url = url.strip()
    ishttps = url.startswith("https://")
    cleaned = url.removeprefix("https://").removeprefix("http://")
    www =  "www." if url.startswith("www.") else ""
    cleaned = cleaned.removeprefix("www.")
    protocol =  "http://"  if url.startswith("https://") or  url.startswith("http://") else ""
    domain,sep,path = cleaned.partition("/")
    addHTTP = ending.URLAdds.HTTPS.value if ishttps else ending.URLAdds.HTTP.value 
    return protocol + www + domain + addHTTP + sep + path 

def despoof_url(url:str)->str : 
    url = url.strip()
    cleaned = url.removeprefix("http://")
    www =  "www." if cleaned.startswith("www.") else ""
    cleaned = cleaned.removeprefix("www.")
    protocol = "https://" if cleaned.endswith(ending.URLAdds.HTTPS.value) else "http://"
    domain = cleaned.strip().removesuffix(ending.URLAdds.HTTPS.value).removesuffix(ending.URLAdds.HTTP.value)
    return protocol + www + domain + "/"

def isSpoofed(url:str)->bool: 
    url = url.strip()
    ishttps = url.startswith("https://")
    cleaned = url.removeprefix("https://").removeprefix("http://")
    www =  "www." if url.startswith("www.") else ""
    cleaned = cleaned.removeprefix("www.")
    domain,sep,path = cleaned.partition("/")
    return (ishttps and domain.endswith(ending.URLAdds.HTTPS.value)) or (not ishttps and domain.endswith(ending.URLAdds.HTTP.value))

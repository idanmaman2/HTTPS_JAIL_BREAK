
from spoofing.urlspoof.ending import URLAdds
def spoof_url(url:str)->str:
    print("url ::: ",url)
    url = url.strip()
    ishttps = url.startswith("https://")
    cleaned = url.removeprefix("https://").removeprefix("http://")
    www =  "www." if url.startswith("www.") else ""
    cleaned = cleaned.removeprefix("www.")
    protocol =  "http://"  if url.startswith("https://") or  url.startswith("http://") else ""
    domain,sep,path = cleaned.partition("/")
    addHTTP = URLAdds.HTTPS.value if ishttps else URLAdds.HTTP.value 
    return protocol + www + domain + addHTTP + sep + path 

def despoof_url(url:str)->str : 
    url = url.strip()
    cleaned = url.removeprefix("http://")
    www =  "www." if cleaned.startswith("www.") else ""
    cleaned = cleaned.removeprefix("www.")
    protocol = "https://" if cleaned.startswith(URLAdds.HTTPS) else "http://"
    domain = cleaned.removeprefix(URLAdds.HTTPS).removeprefix(URLAdds.HTTPS)
    return protocol + www + domain + "/"

def isSpoofed(url:str)->bool: 
    url = url.strip()
    ishttps = url.startswith("https://")
    cleaned = url.removeprefix("https://").removeprefix("http://")
    www =  "www." if url.startswith("www.") else ""
    cleaned = cleaned.removeprefix("www.")
    domain,sep,path = cleaned.partition("/")
    print(domain)
    return domain.endswith(URLAdds.HTTPS.value) or domain.endswith(URLAdds.HTTP.value)


from spoofing.objects.http_ex import HTTP 
from spoofing.urlspoof.spoofer import spoof_url
def http_spoof(httpPack:HTTP):
    httpPack.headers["Location"]=spoof_url(httpPack.headers["Location"])
    return httpPack
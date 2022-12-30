import requests
import datetime
def getHstsHeader(siteName): 
    respone = requests.get(siteName)
    hsts = respone.headers.get("Strict-Transport-Security").split(";")
    if "max-age" in hsts[0]: 
        hsts[0] =datetime.timedelta(seconds= int(hsts[0].split("=")[1])) 
    return hsts 
#print(getHstsHeader("https://www.discountbank.co.il/")[0])




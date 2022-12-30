
import requests
import re 

def is_preLoaded(domainName):
    isLoaded = requests.get(f"https://hstspreload.org/api/v2/status?domain={domainName}").json()
    return isLoaded["status"] == "preloaded"

#print(is_preLoaded("paypal.com"))
#print(is_preLoaded("jct.ac.il"))



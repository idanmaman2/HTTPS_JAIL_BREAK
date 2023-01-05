
import requests

def is_preLoaded(domainName):
    ''' checks if website is preloaded'''
    isLoaded = requests.get(f"https://hstspreload.org/api/v2/status?domain={domainName}").json()
    return isLoaded["status"] == "preloaded"

#print(is_preLoaded("paypal.com"))
#print(is_preLoaded("jct.ac.il"))



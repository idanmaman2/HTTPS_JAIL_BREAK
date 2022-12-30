from flask import Flask,Response, make_response
from flask import request
import requests
from proxyParser import parse
app = Flask(__name__)

Cookies = ["Set-Cookie","content-language","content-type","X-Csrf-Token","Referer"]
def path_disassmale(path): 
    domainPath = path.split("@")
    domain=""
    path=""
    if len(domainPath) == 2 : 
        domain,path = domainPath 
    if len(domainPath) == 1 : 
        domain = domainPath[0]
    return domain,path


@app.route("/<path:path>")
def post_proxy(path): 
    
    domain , sub_path = path_disassmale(path )
    headersRequest ={} 
    for cookieName in Cookies : 
        if cookieName in request.headers : 
            headersRequest[cookieName] = request.headers[cookieName]
    respone = requests.post(domain+sub_path,data=request.form ,headers=headersRequest)
    
    resp = Response(respone.text,status=  respone.status_code)
    if "Set-Cookie" in respone.headers : 
        resp.headers["Set-Cookie"] = respone.headers["Set-Cookie"]
    if "content-language" in respone.headers : 
        resp.headers["content-language"] = respone.headers["content-language"]
    if "content-type" in respone.headers : 
        resp.headers["content-type"] = respone.headers["content-type"]
    return resp
 

@app.route("/<path:path>")
def get_proxy(path):
    """_summary_

    Args:
        path (_type_): pattern in that form 
        http://192.168.230.148:8080/https://github.com@/idanmaman2/
        domain@path 
    Returns:
        _type_: the requested html page on http connection 
    """
    if path == "favicon.ico" :
       path =  request.headers["referer"]+"@/favicon.ico"   
    domain,sub_path = path_disassmale(path)
    respone = requests.get(domain+sub_path)
    if  "content-type" in respone.headers and "image" in respone.headers ["content-type"]: 
         resp =   make_response(respone.content)
         resp.headers.set('Content-Type',respone.headers ["content-type"] )
         resp.headers.set('Content-Disposition', 'attachment', filename=sub_path)
         return resp 
    resp = Response(parse(respone.text,domain))
    if "Set-Cookie" in respone.headers : 
        resp.headers["Set-Cookie"] = respone.headers["Set-Cookie"]
    if "content-language" in respone.headers : 
        resp.headers["content-language"] = respone.headers["content-language"]
    if "content-type" in respone.headers : 
        resp.headers["content-type"] = respone.headers["content-type"]
    return resp

    
if __name__ == "__main__":
    
    app.run(host="0.0.0.0",port=8080)
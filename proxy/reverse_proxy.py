from flask import Flask, request,make_response
import requests

app = Flask(__name__)



@app.route('/proxy', methods=['GET', 'POST'])
def proxy():
    url = request.args.get('url')
    method = request.method
    data = request.form if method == 'POST' else request.args
    respone = requests.request(method, url, data=data)
    returnData = None 
    if "image" in respone.headers['Content-Type'].lower() : 
         resp =   make_response(respone.content)
         resp.headers.set('Content-Type',respone.headers ["content-type"] )
         resp.headers.set('Content-Disposition', 'attachment', filename=sub_path)
         return resp 
    else: 
         return respone.text
    

if __name__ == '__main__':
    app.run()
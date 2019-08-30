from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import datetime
import dht11
import led
import json
import time
import os
import multiprocessing
app = Flask(__name__)
CORS(app, resources={r"/getData": {"origins": "*"}})
CORS(app, resources={r"/lightLed": {"origins": "*"}})
CORS(app, resources={r"/getHistory": {"origins": "*"}})


# @app.route("/")
# def hello():
#     # templateData=dht11();
#     # templateData={
#     # 	'temperature' : 23,
#     # 	'humidity' :30,
#     # }
#     templateData = dht11.calTemp()
#     return render_template("index.html", **templateData)

@app.route("/getData", methods=['GET'])
def home():
    list=[]
    response=dht11.calTemp()
    with open("./data.json",'r+') as f:
        if os.path.getsize('./data.json')==0:
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
    sleepTime=request.args.get("sleepTime")
    lightTime=request.args.get("lightTime")
    p=multiprocessing.Process(target=led.lightLED,args=(sleepTime,lightTime,))
    p.start()
    # led.lightLED(lightTime)
    response={
        'light':'true',
        'sleeptime':sleepTime,
        'lighttime':lightTime,
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,threaded=True)

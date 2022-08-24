import os
from flask import Flask,jsonify,request
import time
from threading import Thread
from bgprocess import *

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

@app.route('/processBG')
def return_status():
    """Return first the response and tie the my_task to a thread"""
    Rurl = (request.args.get('rurl'))
    if len(Rurl)>0:
        Thread(target = my_task,args=(Rurl,)).start()
    if len(Rurl)==0:
        return jsonify(str("No images"))
    Rurl=""
    return jsonify(str("Images detected"))

def my_task(rurl):
    print("rurl Before:  "+rurl)
    bgprocess(rurl)
    print("rurl After:  "+rurl)
    rurl=""
    print("rurl After:  "+rurl)
    return print('large function completed')

import os
from flask import Flask,jsonify,request
import time
from threading import Thread
#from app.bgprocess import *

print("inside")

app = Flask(__name__)

@app.route("/")
def home_view():
    return "Welcome!"

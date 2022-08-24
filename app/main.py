import os
from flask import Flask,jsonify,request
import time
from threading import Thread
#from bgprocess import *

app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

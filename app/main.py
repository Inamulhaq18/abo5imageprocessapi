import os
from flask import Flask,jsonify,request
import time
from threading import Thread
import ayman 
app = Flask(__name__)

@app.route("/")
def main():
    return (ayman.say())

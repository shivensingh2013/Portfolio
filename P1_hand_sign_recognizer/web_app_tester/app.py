from flask import Flask

from flask import Flask, render_template, request, session, render_template_string
import os
from werkzeug.utils import secure_filename
import cv2
import tensorflow.keras.models as tfkm
import numpy as npx
import matplotlib.pyplot as plt
from camera import VideoCamera
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<h1 style='color:green'>Hello World!</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
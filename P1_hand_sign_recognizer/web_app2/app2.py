from flask import Flask, render_template, request, session, render_template_string
import os
import cv2
import tensorflow.keras.models as tfkm
import numpy as np
import matplotlib.pyplot as plt

from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread


##https://towardsdatascience.com/camera-app-with-flask-and-opencv-bd147f6c0eec

global capture,switch, out ,pred
capture=0
switch=1
pred = -1

app = Flask(__name__, template_folder="../web_app2/template" ,static_folder='../web_app2/static')
camera = cv2.VideoCapture(0)

def get_model():
    json_file_path = r"C:\Users\IHG6KOR\Desktop\shiv\Portfolio\shivensingh2013.github.io\P1_hand_sign_recognizer\model_pickle\signdetect.pkl"
    h5_file = r"C:\Users\IHG6KOR\Desktop\shiv\Portfolio\shivensingh2013.github.io\P1_hand_sign_recognizer\model_pickle\signdetect_weights.h5"
    file = open(json_file_path, 'r')
    model_json = file.read()
    file.close()
    new_model = tfkm.model_from_json(model_json)
    # load weights
    new_model.load_weights(h5_file)
    return new_model


## capturing a picture from the video feed
def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success: 
            if(capture):
                capture=0
                now = datetime.datetime.now()
                # p = os.path.sep.join(['static', "shot_{}.png".format(str(now).replace(":",''))])
                # cv2.imwrite(p, frame)
                model = get_model()
                img_npy = frame
                img_npy = cv2.cvtColor(img_npy, cv2.COLOR_BGR2RGB)
                img_npy = cv2.resize(img_npy, (100,100))
                global pred
                pred = np.argmax(model.predict(img_npy.reshape(1,100,100,3)),axis=1)
                print(pred)
                # return render_template('ImageUploadMessage.html',pred = pred)          

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1

        elif  request.form.get('stop') == 'Stop/Start':
            if(switch==1):
                switch=0
                camera.release()
                cv2.destroyAllWindows()
            else:
                camera = cv2.VideoCapture(0)
                switch=1

    elif request.method=='GET':
        return render_template('home.html')
    return render_template('home.html',pred  = pred)

if __name__=='__main__':
    app.run(debug = True)
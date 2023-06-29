from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

global capture,rec_frame, grey, switch, neg, face, rec, out 

capture=0
grey=0
neg=0
face=0
switch=1
rec=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

app = Flask(__name__, template_folder='./template')

camera = cv2.VideoCapture(0)

## for recording the video frame as avi file
# def record(out):
#     global rec_frame
#     while(rec):
#         time.sleep(0.05)
#         out.write(rec_frame)

## capturing a picture from the video feed
def gen_frames():  # generate frame by frame from camera
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            # if(face):                
            #     frame= detect_face(frame)
            # if(grey):
            #     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # if(neg):
            #     frame=cv2.bitwise_not(frame)    
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['static', "shot_{}.png".format(str(now).replace(":",''))])
                print(p)
                cv2.imwrite(p, frame)
            
            # if(rec):
            #     rec_frame=frame
            #     frame= cv2.putText(cv2.flip(frame,1),"Recording...", (0,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),4)
            #     frame=cv2.flip(frame,1)
            
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
    return render_template('index.html')

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
    return render_template('home.html')




if __name__ == '__main__':
    app.run()
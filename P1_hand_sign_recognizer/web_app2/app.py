from flask import Flask, render_template, request, session, render_template_string
import os
from werkzeug.utils import secure_filename
import cv2
import tensorflow.keras.models as tfkm
import numpy as np
import matplotlib.pyplot as plt

#*** Backend operation
 
# WSGI Application
# Defining upload folder path
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
 
# Provide template folder name
# The default folder name should be "templates" else need to mention custom folder name for template path
# The default folder name for static files should be "static" else need to mention custom folder for static path
app = Flask(__name__, template_folder="../web_app2/template" ,static_folder='../web_app2/static')
# Configure upload folder for Flask application
app.config['UPLOAD_FOLDER'] = "../web_app2/static"
 
# Define secret key to enable session
app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    return render_template('home.html')
 
@app.route('/',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        img_file_path = session.get('uploaded_img_file_path', None)
        model = get_model()
        img_npy = cv2.imread(img_file_path)
        img_npy = cv2.cvtColor(img_npy, cv2.COLOR_BGR2RGB)
        img_npy = cv2.resize(img_npy, (100,100))
        pred = np.argmax(model.predict(img_npy.reshape(1,100,100,3)),axis=1)
        
        img_path = "../static/"+str(img_filename)
        print(img_path)
        return render_template('ImageUploadMessage.html',user_image = img_path ,pred = pred)
 

@app.route('/take_pic')
def take_picture():
    return render_template_string('''
<video id="video" width="640" height="480" autoplay style="background-color: grey"></video>
<button id="snap">Take Photo</button>
<canvas id="canvas" width="640" height="480" style="background-color: grey"></canvas>

<script>

// Elements for taking the snapshot
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        //video.src = window.URL.createObjectURL(stream);
        video.srcObject = stream; // assing stream to <video>
        video.play();             // play stream
    });
}

// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
    context.drawImage(video, 0, 0, 640, 480);  // copy video frame to canvas
});

</script>
''')

def get_model():
    json_file_path = r"C:\Users\IHG6KOR\Desktop\shiv\CNN_deeplearning\P1_hand_sign_recognizer\model_pickle\signdetect.pkl"
    h5_file = r"C:\Users\IHG6KOR\Desktop\shiv\CNN_deeplearning\P1_hand_sign_recognizer\model_pickle\signdetect_weights.h5"
    file = open(json_file_path, 'r')
    model_json = file.read()
    file.close()
    new_model = tfkm.model_from_json(model_json)
    # load weights
    new_model.load_weights(h5_file)
    return new_model


if __name__=='__main__':
    app.run(debug = True)





    # @app.route('/show_image')
# def displayImage():
#     # Retrieving uploaded file path from session
#     img_file_path = session.get('uploaded_img_file_path', None)
#     # Display image in Flask application web page
#     return render_template('show_image.html', user_image = img_file_path)
# @app.route('/predict_image')
# def predict_image():
#     # Retrieving uploaded file path from session
#     img_file_path = session.get('uploaded_img_file_path', None)
#     # Display image in Flask application web page
#     model = get_model()
#     img_npy = cv2.imread(img_file_path)
#     img_npy = cv2.cvtColor(img_npy, cv2.COLOR_BGR2RGB)
#     img_npy = cv2.resize(img_npy, (100,100))
#     pred = np.argmax(model.predict(img_npy.reshape(1,100,100,3)),axis=1)
#     return render_template('predict_image.html', pred = pred)
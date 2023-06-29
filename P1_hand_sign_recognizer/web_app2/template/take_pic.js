'''
<video id="video" width="640" height="480" autoplay style="background-color: grey"></video>
<button id="snap">Take Photo</button>
<button id="save">Save Pic</button>
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
download_img = function() {
  // get image URI from canvas object
  var imageURI = canvas.toDataURL("/web_app2/static/image_camera.jpg");
  el.href = imageURI;
};

//Saving the  image on to local 

window.onload = function() {
    // Your javascript code here
    context.drawImage(video, 0, 0, 640, 480);
}


</script>
'''
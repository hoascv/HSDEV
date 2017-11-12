from flask import Blueprint,render_template,flash, redirect, url_for, request, Response
from jinja2 import TemplateNotFound
from hswebapp import app,db
from importlib import import_module
import os
webstreaming = Blueprint('webstreaming', __name__,template_folder='templates')


## import camera driver - READ FROM THE PIC FOLDER
#if os.environ.get('CAMERA'):
#    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
#else:
#    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from hswebapp.camera_pi import Camera




@webstreaming.route('/webstreaming_page1')

def webstreaming_func():
    """Video streaming home page."""
    return render_template('pages/webstreaming.html')
    
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@webstreaming.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


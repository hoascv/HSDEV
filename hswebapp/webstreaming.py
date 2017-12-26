from flask import Blueprint,render_template,flash, redirect, url_for, Response
from jinja2 import TemplateNotFound
from hswebapp import app
from importlib import import_module

from flask_login import login_required,login_user, current_user


streaming = Blueprint('webstreaming', __name__,template_folder='templates/webstreaming/pages')


## import camera driver - READ FROM THE PIC FOLDER
#if os.environ.get('CAMERA'):
#    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
#else:
#    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
from hswebapp.camera_pi import Camera




@streaming.route('/webstreaming_hs')
@login_required
def webstreaming_func():
    """Video streaming home page."""
    return render_template('webstreaming.html')
    
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@streaming.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


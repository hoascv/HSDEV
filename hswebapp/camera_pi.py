import io
import time
import picamera
from picamera import Color
from base_camera import BaseCamera
import datetime as dt

class Camera(BaseCamera):
    @staticmethod
    def frames():
        with picamera.PiCamera() as camera:
            # let camera warm up
            time.sleep(2)

            stream = io.BytesIO()
            camera.annotate_foreground = Color('green')
            camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # return current frame
                stream.seek(0)
                yield stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

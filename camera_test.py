from picamera import PiCamera
from time import sleep

camera = PiCamera()

#set to maximum resolution
camera.resolution = (1920, 1080) #for video
camera.framerate = 15

camera.start_preview()

for i in range(1,5):
    sleep(5)
    print("Picture {} of {}".format(i,5))
    camera.annotate_text = "Hello world!"
    camera.capture('/home/image{}.jpg'.format(i))

camera.stop_preview()

camera.start_preview()
camera.start_recording('/home/video.h264')
camera.wait_recording(5) # better then sleep 

    
camera.stop_recording()
camera.stop_preview()

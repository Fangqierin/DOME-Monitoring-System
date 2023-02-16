from picamera import PiCamera
from time import sleep

camera = PiCamera()

# camera.start_preview()
# sleep(3)
# camera.stop_preview()

# Take picture
# sense light level
sleep(2)
camera.capture('test.jpg')

# Take video
camera.start_recording('test.h264')
sleep(4)
camera.stop_recording()

# Change configuration
camera.resolution(1920, 1080)
camera.framarate = 15
# Add text
camera.annotate_text = "Something"
camera.start_preview()
sleep(2)
camera.capture('clearone.jpg')
camera.stop_preview()

# More in api
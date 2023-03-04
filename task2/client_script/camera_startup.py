from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()

MAX_COUNT = 100
INTERVAL_SEC = 2
cur = datetime.now()
TODAY = f"{cur.month}-{cur.day}"

count = 0
camera.start_preview()

while count < MAX_COUNT:
    sleep(INTERVAL_SEC)
    camera.capture(f'/home/sothis/Documents/archive/{TODAY}_{count}.jpg')
    count += 1

camera.stop_preview()

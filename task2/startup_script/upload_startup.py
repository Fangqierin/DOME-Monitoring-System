import urllib.request
import os
from time import sleep

PHOTO_PATH = '/home/sothis/Documents/archive'
RETRY_INTERVAL_SEC = 60

# return true if the server is accessable
def conn_check():
    try:
        url = "https://www.google.com"
        urllib.request.urlopen(url)
        # status = "Connected"
    except Exception as e:
        print(e)
        return False

    return True

# return true is there are files to be uploaded
def dir_isEmpty():
    dir = os.listdir(PHOTO_PATH)
    return len(dir) != 0

# regularly check internet condition and upload data as need
def run():
    while True:
        if not dir_isEmpty() and conn_check():
            # TODO: upload data
            pass
        else:
            sleep(RETRY_INTERVAL_SEC)

        


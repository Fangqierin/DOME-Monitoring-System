from config import *

import zmq
import os
import time
import subprocess

context = zmq.Context()

# create a ZMQ PUB socket
socket = context.socket(zmq.PUB)
socket.connect(f"tcp://{SERVER_HOST}:{ZMQ_PORT}")


def conn_check() -> bool:
    # Run the command to get the SSID of the currently connected network
    result = subprocess.run(['iwgetid', '-r'], capture_output=True, text=True)

    # Extract the SSID from the output
    ssid = result.stdout.strip()

    # Check if the SSID is empty
    if not ssid:
        print("Not currently connected to a WiFi network")
        return False
    else:
        print(f"Currently connected to WIFI with ssid: {ssid}")
        return ssid == wifi_name


# set the topic for this publisher
topic = ZMQ_TOPIC

while True:
    # comment this section if not running on raspberry pi
    if not conn_check():
        time.sleep(RETRY_INTERVAL_SEC)
        continue

    # scan the folder and upload all files with the given topic
    for filename in os.listdir(folder_path):
        if filename.endswith(file_ends):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "rb") as f:
                data = f.read()

            try:
                # send the data to the subscriber with the given topic
                socket.send_multipart([topic.encode(), filename.encode(), data])
                print(f"Published {filename} on topic {topic}")
            except zmq.ZMQError as e:
                print(f"Error: {e}, retrying in 5 seconds")
                time.sleep(RETRY_INTERVAL_SEC)
                break

            os.remove(filepath)

    time.sleep(SCAN_INTERVAL_SEC)

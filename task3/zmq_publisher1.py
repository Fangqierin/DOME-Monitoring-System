from config1 import *

import zmq
import os
import time

context = zmq.Context()

# create a ZMQ PUB socket
socket = context.socket(zmq.PUB)
socket.connect(f"tcp://{SERVER_HOST}:{ZMQ_PORT}")

# set the topic for this publisher
topic = ZMQ_TOPIC

while True:
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

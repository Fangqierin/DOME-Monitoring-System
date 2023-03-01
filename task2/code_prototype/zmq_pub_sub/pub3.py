from config import *

import zmq
import os
import time

context = zmq.Context()

# create a ZMQ PUB socket
socket = context.socket(zmq.PUB)
socket.connect(f"tcp://{ZMQ_HOST}:{ZMQ_PORT}")

# set the topic for this publisher
topic = ZMQ_TOPICS[2]

while True:
    # scan the folder and upload all files with the given topic
    for filename in os.listdir(folder_path[2]):
        filepath = os.path.join(folder_path[2], filename)
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

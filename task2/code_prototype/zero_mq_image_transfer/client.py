from config import *

import zmq
import os
import time

# Set up the ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.RCVTIMEO, 1000)  # timeout
socket.connect(f"tcp://{server_ip}:{server_port}")  # replace with the IP address of your server

# Set up the folder to watch
folder_to_watch = folder_path  # replace with the path to the folder you want to watch


def reset_socket():
    global socket
    socket.close()
    socket = context.socket(zmq.REQ)
    socket.setsockopt(zmq.RCVTIMEO, 1000)  # timeout
    socket.connect(f"tcp://{server_ip}:{server_port}")  # replace with the IP address of your server


# Infinite loop to watch the folder and send images
while True:
    print("Start scanning")
    try:
        for filename in os.listdir(folder_to_watch):
            if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                print(f"Uploading {filename}")
                # Open the image file and read its contents
                with open(os.path.join(folder_to_watch, filename), "rb") as f:
                    image_contents = f.read()

                # Send the image filename and contents to the server
                socket.send_multipart([filename.encode(), image_contents])

                # Wait for the server to respond
                response = socket.recv()

                # Print the response
                print(response)

                # Remove the image file from the folder
                os.remove(os.path.join(folder_to_watch, filename))

        print("Scan finished")
        time.sleep(scan_interval)
    except zmq.ZMQError as e:
        print(e)
        time.sleep(retry_interval)
        reset_socket()

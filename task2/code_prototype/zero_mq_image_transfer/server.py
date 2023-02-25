from config import *

import zmq

# Set up the ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{server_port}") # listen on all available network interfaces

# Infinite loop to receive images
while True:
    # Wait for an image and filename to arrive from a client
    filename, image_contents = socket.recv_multipart()

    # Save the image to a file with the original filename
    with open(filename.decode(), "wb") as f:
        f.write(image_contents)

    # Send a response back to the client
    socket.send(b"Image received and saved successfully.")
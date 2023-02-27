from pymongo import MongoClient
from config import *

import zmq

# Set up the ZeroMQ context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{server_port}") # listen on all available network interfaces

# Set up the db context
client = MongoClient(
    f"mongodb+srv://{username}:{password}@forumdb.cc36b.mongodb.net/?retryWrites=true&w=majority"
)
db = client["img_receiver"]
collection = db["test"]

# Infinite loop to receive images
while True:
    # Wait for an image and filename to arrive from a client
    filename, image_contents = socket.recv_multipart()

    # Upload the image to mongodb
    image = {"filename": filename.decode(), "contents": image_contents}
    collection.insert_one(image)

    # Send a response back to the client
    socket.send(b"Image received and saved successfully.")
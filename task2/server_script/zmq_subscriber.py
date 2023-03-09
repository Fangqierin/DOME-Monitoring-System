from config import *

import os
import zmq
import pymongo

context = zmq.Context()

# create a ZMQ SUB socket and subscribe to all topics
socket = context.socket(zmq.SUB)
socket.bind(f"tcp://*:{ZMQ_PORT}")
socket.setsockopt_string(zmq.SUBSCRIBE, "")  # filter here

if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# connect to MongoDB
client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB_NAME]

while True:
    # receive the topic and data from the publisher
    topic, filename, data = socket.recv_multipart()
    topic = topic.decode()
    filename = filename.decode()

    if topic == "images":
        # save the image locally in the IMAGE_DIR
        filepath = os.path.join(IMAGE_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(data)
        # insert the file path into the corresponding collection in MongoDB
        collection = db[topic]
        collection.insert_one({"filename": filename})
    else:
        # insert the data into the corresponding collection in MongoDB
        collection = db[topic]
        collection.insert_one({"filename": filename, "data": data.decode()})

    # print out a confirmation message
    print(f"Received {len(data)} bytes on topic {topic}")

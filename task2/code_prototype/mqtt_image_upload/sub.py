import os

import paho.mqtt.client as paho
from paho import mqtt
from config import username, password, broker_address


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# Dictionary to store the received chunks
chunks = {}


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    if msg.topic.startswith("encyclopedia/image/"):
        # Extract the sequence number and image name from the topic
        _, _, image_name, seq_num = msg.topic.split("/")
        seq_num = int(seq_num)

        if image_name not in chunks:
            chunks[image_name] = {}

        # If the chunk is the EOF (End Of File) marker, write the chunks to the output file
        if msg.payload == b"EOF":
            save_path = "received_" + image_name
            with open(save_path, "wb") as f:
                for i in range(len(chunks[image_name])):
                    f.write(chunks[image_name][i])
            print(f"Received all the chunks of the image {image_name} (seq_num={seq_num})")
            chunks[image_name].clear()  # Clear the dictionary
        else:
            # Store the chunk in the dictionary
            chunks[image_name][seq_num] = msg.payload
            print(f"Received a chunk of the image {image_name} (seq_num={seq_num})")
    else:
        print(msg.payload)


# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(username, password)

# setting callbacks, use separate functions like above for better visibility
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message

# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(broker_address, 8883)
# subscribe to all topics of encyclopedia by using the wildcard "#"
client.subscribe("encyclopedia/#", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
client.loop_forever()

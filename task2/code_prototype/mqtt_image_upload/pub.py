import os
import paho.mqtt.client as paho
from paho import mqtt
from config import username, password, broker_address


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


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
client.on_publish = on_publish


# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(broker_address, 8883)
# client.publish("encyclopedia/test", "something")

CHUNK_SIZE = 1024  # Define the size of each chunk in bytes

# Define the path to the JPG file to send
file_path = "image.jpg"

with open(file_path, "rb") as f:
    seq_num = 0
    while True:
        chunk = f.read(CHUNK_SIZE)  # Read a chunk of bytes from the file
        if not chunk:  # If there are no more bytes to read, break out of the loop
            client.publish(f"encyclopedia/image/{os.path.basename(file_path)}/-1", b"EOF")
            break
        client.publish(f"encyclopedia/image/{os.path.basename(file_path)}/{seq_num}", chunk)
        seq_num += 1

client.loop_forever()

import urllib.request
import os
import paho.mqtt.client as paho
from paho import mqtt
from time import sleep
from config import username, password, broker_address

# Define the folder to watch
folder_path = '/home/sothis/Documents/archive'
# Define the interval between scans, in seconds
scan_interval = 10
# Define the interval between internet checks, in seconds
retry_interval = 20


# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))


# MQTT setup
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(username, password)
client.connect("53830014e96a4b8992bbbff1c85161c8.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
client.on_connect = on_connect
client.on_publish = on_publish

# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(broker_address, 8883)


# return true if the server is accessable
def conn_check():
    try:
        url = "https://www.google.com"
        urllib.request.urlopen(url)
        # status = "Connected"
    except Exception as e:
        print(e)
        sleep(retry_interval)
        return False

    return True


# regularly check internet condition and upload data as need
while True:
    if conn_check():
        if not client.is_connected:
            client.reconnect()
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".jpg"):
                file_path = os.path.join(folder_path, file_name)
                with open(file_path, "rb") as f:
                    # Send the file in chunks
                    CHUNK_SIZE = 1024
                    seq_num = 0
                    while True:
                        chunk = f.read(CHUNK_SIZE)
                        if not chunk:
                            client.publish(f"encyclopedia/image/{file_name}/-1", b"EOF")
                            break
                        client.publish(f"encyclopedia/image/{file_name}/{seq_num}", chunk)
                        seq_num += 1
                # Delete the file after sending it
                os.remove(file_path)
        client.loop(scan_interval)

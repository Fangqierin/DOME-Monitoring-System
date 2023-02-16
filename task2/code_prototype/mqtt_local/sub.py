import client_config

from paho.mqtt import client as mqtt_client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(client_config.topic)
    client.on_message = on_message


def run():
    client = client_config.connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

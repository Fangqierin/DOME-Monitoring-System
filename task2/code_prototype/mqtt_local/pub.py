import time
import client_config


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(client_config.topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{client_config.topic}`")
        else:
            print(f"Failed to send message to topic {client_config.topic}")
        msg_count += 1


def run():
    client = client_config.connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

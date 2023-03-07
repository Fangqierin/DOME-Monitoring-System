# Task 2: Explore store-and-upload data transmission

## Description

This folder contains the code running on the testing raspberry pi. The file location maybe different on other machines.

Find details task descriptions [here](https://trello.com/c/9CVeJohe/18-task2-week4).

**client_script**

> The scripts in this folder run automatically when the machine is turned on.
> * camera_startup.py
> 
>   Automatically start taking photos and saving to local storage by setting interval.
> * upload_startup.py
> 
>   Automatically start checking existed data and network condition. Publish data to the port using zmq.
> 
> * zmq_publisher.py
> 
>   Publish to the port.

**server_script**

> The scripts in this folder runs on the server side.
> * zmq_subscriber.py
> 
>   Subscribe to the port, handle incoming data and save them to local mongodb. (Images will be saved to local storage and only file path will be saved to mongodb)
> * db_handler.py
> 
>   Provide APIs to query data from mongodb.


## Usage


### How to host dashboard in local network
Run `server_script/db_handler.py` to host the api server.

Host web client following Readme in `dome_dashboard` folder.


### How to transfer data using zmq in other project
Run `server_script/zmq_subscriber.py` to host a subscriber locally.

Run `client_script/upload_startup.py` to host a publisher on your raspberrypi or zmq_publisher.py on a non-linux device.

The publisher will check connection, scan the folder to upload files.

The subscriber will save the data to mongodb

Configuration file example can be found in README at that folder

## Common problems

**Black screen when setting up the raspberrypi**

It might because the monitor isn't compatible with the monitor. Try [this solution](https://raspberrypi.stackexchange.com/questions/7009/will-not-boot-black-screen-only).


**Raspberry pi camera commands**

[Tutorial](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)



**Set Raspberry pi startup script**

Edit `/etc/rc.local`

Add a new line to call the script

**Note** The file runs as root, you need to install the packages as root using sudo.

```sudo python /home/pi/sample.py &```

Must contain a *&* if the script won't end automatically.

**MQTT doesn't work when sending large file**

Use chunks. we changed to zeroMQ for image transfer.


**Add networks and switch between them**

Edit `/etc/wpa_supplicant/wpa_supplicant.conf` and set different priority to each netwsudo

Example:
```
network={
    ssid="SCHOOLS NETWORK NAME"
    psk="SCHOOLS PASSWORD"
    priority=1
}
```

Larger priority is accessed 1st.

Use
`wpa_cli -i wlan0 select_network 0` to switch to the 1st.

PS: after call the command, until reboot or manually cancelled using `wpa_cli -i wlan0 enable_network all`, other networks will be disabled.

If can't access using hostname, access the router to find the ipaddress of raspberry pi, then ssh to it using ip address instead of hostname.


*Find mongodb ip*
use db.runCommand({whatsmyuri: 1}) after selecting a database in mongosh




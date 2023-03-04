# Task 2: Explore store-and-upload data transmission

### Description

The task 2 contains several stages:

1. Week 1
   
   * Set up env and camera accessory. 
   
   * Take photos using command line and python script.

2. Week 2
   
   * Edit startup setting to run the scripts automatically.
   
   * Create a simulating environment to send image using mqtt.
   
   * Add a feature to check internet status. Store images at local when the internet is unavailable and retry when it's available again.



This folder contains the code running on the testing raspberry pi. The file location maybe different on other machines.

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


### How to apply it to other project
Run `code_prototype/zmq_pub_sub/sub.py` to host a subscriber locally.

Run `startup_script/upload_startup.py` to host a publisher on your device.

The publisher will check connection, scan the folder to upload files.

The subscriber will save the data to mongodb

To simulate multiple publisher, you can run files in zmq_pub_sub at the same time.


### Common problems

**Black screen when set up the raspberrypi**

It might because the monitor isn't compatible with the monitor. Try [this solution](https://raspberrypi.stackexchange.com/questions/7009/will-not-boot-black-screen-only).


**Camera commands**

[Tutorial](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)



**Startup script**

Edit `/etc/rc.local`

Add a new line to call the script

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




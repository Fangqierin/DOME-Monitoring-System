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

**startup_script**

> The scripts in this folder run automatically when the machine is turned on.
> * camera_startup.py
> 
>   Automatically start taking photos and saving to local storage by setting interval.
> * upload_startup.py
> 
>   Automatically start checking existed data and network condition. Upload data to server.

**code_prototype**

> The scripts in this folder serves as a rough unit test for the function that will be used in real scripts.



### Common problems

**Black screen when set up the raspberrypi**

It might because the monitor isn't compatible with the monitor. Try [this solution](https://raspberrypi.stackexchange.com/questions/7009/will-not-boot-black-screen-only).



**Camera commands**

[Tutorial](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera/0)



**Startup script**

Edit /etc/rc.local

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

Access the router to find the ipaddress of raspberry pi, then ssh to it using ip address instead of hostname.

Why not use hostname: when connecting to a new network, need to edit the config on the router side, it would be more convenient to use a phone of laptop to find the ip address.








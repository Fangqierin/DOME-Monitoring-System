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

**startup.py**

> The script runs automatically when the machine is turned on.

### 



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











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

**code_prototype**

> The scripts in this folder serves as a rough unit test for the function that will be used in real scripts.
> * camera_startup.py
> 
>   Automatically start taking photos and saving to local storage by setting interval.
> * upload_startup.py
> 
>   Automatically start checking existed data and network condition. Upload data to server.
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











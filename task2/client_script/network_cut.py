import os
import time

# Turn off WiFi
os.system("sudo ifconfig wlan0 down")
print("WiFi turned off.")

# Wait for one minute
time.sleep(60)

# Reconnect WiFi
os.system("sudo ifconfig wlan0 up")
print("WiFi reconnected.")
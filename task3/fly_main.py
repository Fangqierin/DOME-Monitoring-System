"""
Main file meant for execution that will run the program and
make the drones fly around the given waypoints
"""

from tello_drone import Tello_drone
from grid import Grid
import time
import pygame
import os
import asyncio
import cv2
import signal

running = True

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        running = False
 
signal.signal(signal.SIGINT, handler)

if __name__ == "__main__":
    # The grid is turned off for now for performance
    # grid
    # grid = Grid(main_drone)
    try:
        # pygame.init()
        # screen = pygame.display.set_mode((900, 600))

        main_drone = Tello_drone(0, -50)
        main_drone.takeoff()

        while running:
            if len(main_drone.waypoints) > 0: 
                w = main_drone.waypoints.pop()
                print(w)
                main_drone.prev_waypoint = main_drone.current_waypoint
                main_drone.current_waypoint = w
                main_drone.move()
                #main_drone.waypointsCollection.update_one({"_id":main_drone.current_waypoint["_id"]},{"$set":{"read":"1"}})
            main_drone.add_waypoints_database()

    finally:
        main_drone.land()
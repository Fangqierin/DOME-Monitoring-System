"""
Main file meant for execution that will run the program and
make the drones fly around the given waypoints
"""

from tello_drone import Tello_drone
#from grid import Grid
import time
import pygame
import os
import asyncio
import cv2
import signal
import time
import sys



def signal_handler(signal, frame):
    global running
    print("INTERUPTED")
    running = False

signal.signal(signal.SIGINT, signal_handler)

running = True

if __name__ == "__main__":
    # The grid is turned off for now for performance
    # grid
    # grid = Grid(main_drone)
    try:
        # pygame.init()
        # screen = pygame.display.set_mode((900, 600))

        main_drone = Tello_drone(25, 25, 90)
        main_drone.takeoff()
        main_drone.add_waypoints_database()


        # while running:
        #     if len(main_drone.waypoints) > 0: 
        #         w = main_drone.waypoints.pop()
        #         print(w)
        #         main_drone.prev_waypoint = main_drone.current_waypoint
        #         main_drone.current_waypoint = w
        #         main_drone.move_direct()
        #         #main_drone.waypointsCollection.update_one({"_id":main_drone.current_waypoint["_id"]},{"$set":{"read":"1"}})
        #     else:
        #         main_drone.add_waypoints_database()

        for _ in range(sys.argv[1]): #number of rounds
            for w in main_drone.waypoints:
                #w = main_drone.waypoints[i]
                print(w)
                main_drone.prev_waypoint = main_drone.current_waypoint
                main_drone.current_waypoint = w
                #main_drone.move()
                main_drone.move_direct()
                #w_i = i

            main_drone.prev_waypoint = main_drone.current_waypoint
            main_drone.current_waypoint = main_drone.base_waypoint # comes to base to check if there are new waytpoints
            print("returning to base ", main_drone.current_waypoint)
            main_drone.move_direct()
            time.sleep(5)

            main_drone.add_waypoints_database()
            # for i in range(w_i+1, main_drone.total_waypoints):
            #     w = main_drone.waypoints[i]
            #     print(w)
            #     main_drone.prev_waypoint = main_drone.current_waypoint
            #     main_drone.current_waypoint = w
            #     main_drone.move_direct()

        print("landing")
        main_drone.land()
    finally:
        #pass
        print("exception landing")
        main_drone.land()
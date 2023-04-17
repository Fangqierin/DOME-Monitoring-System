# Task 3: Event-Driven FLight Path Generation

## Description

This folder contains the code for running the Tello drone. The drone captures images and processes images to detect fires in them. And sends the fire details to the server.

## File functions

fly_main.py : main file to fly the drone given the waypoints in the database (moongodb)

tello_drone.py : functions to control the tello drone

image_processing : functions to extract and return fire details such as size and location from images

play_mongo.py : file to intialize mongodb

random_insert.py : function to insert a waypoin to the database when the drone is flying to test Event-Driven FLight Path Generation

# USED TO INSERT A WAYPOINT INTO THE MONGODB WHEN THE DRONE IS IN FLIGHT TO CHECK
# IF EVENT DRIVEN PATH GENERATION WORKS

from glob import glob
from pymongo import MongoClient


def add_waypoints_database(currRound):
        # adds all of the waypoints from the database (client)

        waypoints = list(client["waypoints"].currentWaypoints.find({"Round": str(currRound)}))

        print("read waypoints", len(waypoints))

        for waypoint in waypoints:
            new_waypoint = (int(waypoint['x']),int(waypoint['y']),int(waypoint['z']))
            print("new waypoint ", new_waypoint)

            self.waypoints.append(new_waypoint)
        
        # The first element of the list is the dummy initial waypoint so we skip it
        if len(waypoints) == 0: return False

        self.waypoints.append(self.waypoints[0])

        return True


def insert_mongo(col):
	col.insert_many([{"read": "0","x": "-80", "y": "-80", "z": "110" },])



client = MongoClient("mongodb://127.0.0.1:27017/")


# Create database called waypoints
waypointsdb = client["waypoints_new"]
# Create Collection (table) called currentWaypoints
waypointsCollection = waypointsdb.currentWaypoints

insert_mongo(waypointsCollection)


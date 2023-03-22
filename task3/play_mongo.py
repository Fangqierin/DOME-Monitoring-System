# USED TO INITIALISE THE MONGODB

# from os import remove
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
	col.insert_many([{"read": "0","x": "0", "y": "-25", "z": "110" },
                                    {"read": "0", "x": "50", "y": "-25", "z": "110" },
                                    {"read": "0", "x": "50", "y": "25", "z": "110" },
                                    {"read": "0", "x": "-50", "y": "25", "z": "110"},
                                  ])


client = MongoClient("mongodb://127.0.0.1:27017/")


# Create database called waypoints
waypointsdb = client["waypoints_new"]
# Create Collection (table) called currentWaypoints
waypointsCollection = waypointsdb.currentWaypoints

imagedb = client["images"]
imageCollection = imagedb.currentImages


imageCollection.delete_many({})
waypointsCollection.delete_many({})
insert_mongo(waypointsCollection)

# waypoints = list(waypointsCollection.find({"read": "0"}))

# for w in waypoints:
# 	print(w)
# 	waypointsCollection.update_one({"_id":w["_id"]},{"$set":{"read":"1"}})

# insert_mongo2(waypointsCollection)


# waypoints = list(waypointsCollection.find())
# print(waypoints)







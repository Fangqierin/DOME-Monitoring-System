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
	col.insert_many([{"order": "0","x": "25", "y": "25", "z": "100" },
                    {"order": "1", "x": "75", "y": "25", "z": "100" },
                    {"order": "2", "x": "125", "y": "25", "z": "100" },
                    {"order": "3", "x": "125", "y": "75", "z": "100" },
                    {"order": "4", "x": "75", "y": "75", "z": "100" },
                    {"order": "5", "x": "25", "y": "75", "z": "100" },
                    {"order": "6", "x": "25", "y": "125", "z": "100" },
                    {"order": "7", "x": "75", "y": "125", "z": "100" },
                    {"order": "8", "x": "125", "y": "125", "z": "100" },
                    {"order": "9", "x": "125", "y": "175", "z": "100" },
                    {"order": "10", "x": "75", "y": "175", "z": "100" },
                    {"order": "11", "x": "25", "y": "175", "z": "100" },
                    {"order": "12", "x": "25", "y": "25", "z": "100" },
                    {"order": "13", "x": "125", "y": "175", "z": "100" }
                    ])
    # col.insert_many([{"order": "0","x": "100", "y": "100", "z": "100" },
    #                 {"order": "1", "x": "0", "y": "100", "z": "100" },
    #                 {"order": "2", "x": "100", "y": "0", "z": "100" },
    #                 ])        


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







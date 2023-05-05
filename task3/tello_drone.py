
'''
File with the Tello_drone class which represents tello drone objects
and saves additional information about them such as their 
location, speed, waypoints, etc. while also including the implementation
of how and where they should move
'''

'''
This class uses DYNAMICALLY generated paths: all paths are generated
as the drone flies
'''

'''
Limitations: 
1. All coordinates should be divisible by the speed * interval to reduce rounding as much
as possible
2. Drone will fly incorrectly at low speeds
3. Drone flies differently at different altitudes (higher altitudes = higher speed)
4. The speed of the program also affects drone flight
'''

from djitellopy import tello 
import json
import math
import time
import cv2
from glob import glob

from play_mongo import client 

from image_processing import detect_fire
from image_processing import calc_location_fire
import requests

from datetime import datetime;
import json


class Tello_drone:

    # NOTE: COORDINATES ARE MEASURED IN CM
    def __init__(self, i_x: int = 0, i_y: int = 0, i_z: int = 90,):
        #linear_speed: float = 8.0, angular_speed: float = 36.0, 
        #interval: float =  10.0/8.0, yaw = 0):

        # drone
        self.drone = tello.Tello()
        self.drone.connect()
        #self.drone.set_speed(30)
        
        self.drone.streamon()

        # coordinates
        self.x = i_x
        self.y = i_y

        # NOTE: z will be assumed by default to be at a height of 80 cm
        # because that is the takeoff altitude and we want the drone the
        # first waypoint to be its starting position after takeoff
        self.z = i_z

        # # current angle (in degrees) the drone is traveling in
        self.angle = 0

        self.image_no = 0
        self.fire_no = 0

        # list of waypoints the drone must fly to
        # includes the start as the first waypoint
        self.total_waypoints = 0
        self.waypoints = []
        self.base_waypoint = {'x': '0', 'y': '0', 'z': '100'}

        # the current waypoint the drone is on
        self.prev_waypoint = {'x': '0', 'y': '0', 'z': '100'}
        self.current_waypoint = {'x': '0', 'y': '0', 'z': '100'}

        self.x = int(self.current_waypoint["x"])
        self.y = int(self.current_waypoint["y"])
        self.z = int(self.current_waypoint["z"])

        self.waypointsdb = client["waypoints_new"]
        # Create Collection (table) called currentWaypoints
        self.waypointsCollection = self.waypointsdb.currentWaypoints

        self.imagedb = client["images"]
        self.imageCollection = self.imagedb.currentImages

        # # the total distance to the next waypoint in terms of left right foward backward
        # self.current_path_distance_xy = 0

        # # the total distance to the next waypoint in terms of up and down
        # self.current_path_distance_z = 0

        # # the distance the drone has traveled on the current path in terms of left right foward backward
        # self.current_path_traveled_xy = 0

        # # the distance the drone has traveled on the current path in terms of up and down
        # self.current_path_traveled_z = 0

        # # linear and vertical speed of the drone 
        # self.lspeed = linear_speed

        # # angular speed of the drone 
        # self.aspeed = angular_speed

        # # interval between commands
        # self.interval = interval

        # # how much distance the drone covers in left right foward backward up and down each interval
        # self.change = self.lspeed * self.interval

        # self.yaw = yaw


    def takeoff(self):
        # connects the drone and makes it takeoff
        # makes drone fly to designated start height
        self.z = 80
        self.drone.send_control_command("takeoff", timeout = 30)
        #self.drone.takeoff()
        # for _ in range(abs(round((initial_height - 90)/self.change))+1):
        #     self.move(False)
        # if initial_height > 90:
        #     self.drone.move_up(initial_height - 90)
        # elif initial_height < 90:
        #     self.drone.move_down(90 - initial_height)

        # waypoints cannot be empty
        #self.waypoints.insert(0,(0,0,90))


    def land(self):
        # lands the drone
        self.z = 0
        self.drone.land()
        self.drone.streamoff()

    def add_waypoints_database(self):
        # adds all of the waypoints from the database (client)
        ##FROM MONGO WITH SEQUENCE
        # new_waypoints = list(self.waypointsCollection.find())
        # if len(new_waypoints) > 0:
        #     for w in new_waypoints:
        #         self.waypoints[int(w["order"])] = w
        #         self.total_waypoints = max(self.total_waypoints, int(w["order"])+1)

        ##FROM MONGO OLD
        # new_waypoints = list(self.waypointsCollection.find({"read": "0"}))
        # if len(new_waypoints) > 0:
        #     for w in new_waypoints:
        #         self.waypointsCollection.update_one({"_id":w["_id"]},{"$set":{"read":"1"}})
        #     self.waypoints = self.waypoints + new_waypoints
        #     return True
        # else:
        #     self.waypoints.append({"read": "0", "x": "0", "y": "0", "z": "100" })
        #     return False

        ## FROM SERVER
        url = "http://localhost:5555/waypoint"
        response = requests.get(url)
        new_waypoints = response.json()
        if len(new_waypoints) > 0:
            for w in new_waypoints:
                self.waypoints = new_waypoints
                self.total_waypoints += 1

                    
        # FOR LATER
        # FUNCTION THAT WILL SORT WAYPOINTS IN A MATTER
        # SUCH THAT THE LEAST AMOUNT OF DISTANCE IS 
        # TRAVELED
        # self.sort_waypoints()
    

    def reset_waypoints(self):
        '''
        Resets waypoints but keeps the first one
        '''
        if len(self.waypoints) == 0: return
        self.waypoints = [self.waypoints[0]]


    def move(self):
        '''
        Moves the drone along the current path
        '''

        '''
        NOTE: THIS IS NOT THE MOST EFFICIENT IMPLEMENTATION
        THIS IS SIMPLY THE EASIEST IMPLEMENTATION

        INSTEAD OF MOVING ALONG THE 3D VECTOR BETWEEN TWO POINTS, 
        DUE TO ROUNDING LIMITATIONS OUR DRONE WILL JUST MOVE SEPERATELY
        BETWEEN ITS X AND Y MOVEMENT VS ITS Z MOVEMENT INSTEAD OF MOVING
        WITH RESPECT TO ALL 3 AT THE SAME TIME

        IF THE DRONE REACHES ONE X AND Y BEFORE IT REACHES Z IT WILL JUST
        PURELY FLY IN THE Z DIRECTION TO CORRECT THIS AND VICE VERSA
        '''
        
        # if we reach the next waypoint

        # updating which path we are on
        

        l_r_distance = int(self.current_waypoint["x"]) - int(self.prev_waypoint["x"]) 
        b_f_distance = int(self.current_waypoint["y"]) - int(self.prev_waypoint["y"])
        u_d_distance = int(self.current_waypoint["z"]) - int(self.prev_waypoint["z"])

        if abs(l_r_distance) >= 20:
            self.drone.send_control_command("{} {}".format('right' if l_r_distance >=0 else 'left', abs(l_r_distance)),timeout = 40)
            self.x += l_r_distance
        elif abs(l_r_distance) > 0:
            for _ in range(l_r_distance//10):
                self.drone.send_rc_control(10 * (1 if l_r_distance >=0 else -1),0,0,0)
                time.sleep(1)
            self.drone.send_rc_control(0,0,0,0)
        self.x = int(self.current_waypoint["x"])

        if abs(b_f_distance) >= 20:
            self.drone.send_control_command("{} {}".format('forward' if b_f_distance >=0 else 'back', abs(b_f_distance)),timeout = 40)
        elif abs(b_f_distance) > 0:
            for _ in range(b_f_distance//10):
                self.drone.send_rc_control(0,10 * (1 if l_r_distance >=0 else -1),0,0)
                time.sleep(1)
            self.drone.send_rc_control(0,0,0,0)
        self.y = int(self.current_waypoint["y"])
        if abs(u_d_distance) >= 20:
            self.drone.send_control_command("{} {}".format('up' if u_d_distance >=0 else 'down', abs(u_d_distance)),timeout = 40)
        elif abs(u_d_distance) > 0:
            for _ in range(u_d_distance//10):
                self.drone.send_rc_control(0,0,10 * (1 if l_r_distance >=0 else -1),0)
                time.sleep(1)
            self.drone.send_rc_control(0,0,0,0)
        self.z = int(self.current_waypoint["z"])

        self.hover()
        ix = self.upload_current_frame()
        self.upload_fire_details(ix)


    #FAILED
    # def move_direct(self):

    #     x_d = int(self.current_waypoint["x"]) - int(self.prev_waypoint["x"]) # distance to travel in x coordinate
    #     y_d = int(self.current_waypoint["y"]) - int(self.prev_waypoint["y"])
    #     z_d = int(self.current_waypoint["z"]) - int(self.prev_waypoint["z"])

    #     d = math.sqrt(x_d**2 + y_d**2)

    #     x_v = int(round(math.sqrt( ((x_d**2)/(x_d**2 + y_d**2)) * 30)))
    #     y_v = int(round(math.sqrt( ((y_d**2)/(x_d**2 + y_d**2)) * 30)))

    #     x_dir = 1 if x_d >=0 else -1
    #     y_dir = 1 if y_d >=0 else -1

    #     # cmd = 'rc {} {} {} {}'.format(
    #     #     x_v * x_dir,
    #     #     y_v * y_dir,
    #     #     0,
    #     #     0
    #     # )

    #     print(x_v * x_dir)
    #     print(y_v * y_dir)
    #     print("time ", d/30)

    #     self.drone.send_rc_control(x_v * x_dir, y_v * y_dir,0,0)
    #     #self.drone.send_command_with_return(self, cmd, timeout=7)
    #     time.sleep(d/30)
    #     self.drone.send_rc_control(0,0,0,0)

    #     #self.drone.send_control_command("{} {}".format('up' if z_d >=0 else 'down', abs(z_d)),timeout = 40)

    def move_direct(self):

        l_r_distance = int(self.current_waypoint["x"]) - int(self.prev_waypoint["x"]) 
        b_f_distance = int(self.current_waypoint["y"]) - int(self.prev_waypoint["y"])
        u_d_distance = int(self.current_waypoint["z"]) - int(self.prev_waypoint["z"])

        if abs(l_r_distance) >= 10 and b_f_distance == 0:
            self.drone.send_control_command("{} {}".format('right' if l_r_distance >=0 else 'left', abs(l_r_distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)

        elif abs(b_f_distance) >= 10 and l_r_distance == 0:
            self.drone.send_control_command("{} {}".format('forward' if b_f_distance >=0 else 'back', abs(b_f_distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)
        
        elif l_r_distance > 0 and b_f_distance > 0:
            distance = math.sqrt(l_r_distance**2 + b_f_distance**2)
            degrees = math.degrees(math.atan(l_r_distance/b_f_distance))
            self.drone.rotate_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)
            self.drone.send_control_command("{} {}".format('forward', int(distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)
            self.drone.rotate_counter_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)

        elif l_r_distance < 0 and b_f_distance > 0:
            distance = math.sqrt(l_r_distance**2 + b_f_distance**2)
            degrees = math.degrees(math.atan(-l_r_distance/b_f_distance))
            self.drone.rotate_counter_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)
            self.drone.send_control_command("{} {}".format('forward', int(distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)
            self.drone.rotate_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)

        elif l_r_distance > 0 and b_f_distance < 0:
            distance = math.sqrt(l_r_distance**2 + b_f_distance**2)
            degrees = math.degrees(math.atan(-l_r_distance/b_f_distance))
            self.drone.rotate_counter_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)
            self.drone.send_control_command("{} {}".format('back', int(distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)
            self.drone.rotate_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)

        elif l_r_distance < 0 and b_f_distance < 0:
            distance = math.sqrt(l_r_distance**2 + b_f_distance**2)
            degrees = math.degrees(math.atan(l_r_distance/b_f_distance))
            self.drone.rotate_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)
            self.drone.send_control_command("{} {}".format('back', int(distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)
            self.drone.rotate_counter_clockwise(int(degrees))
            self.drone.send_rc_control(0,0,0,0)

        
        self.x = int(self.current_waypoint["x"])
        self.y = int(self.current_waypoint["y"])

        if abs(u_d_distance) >= 20:
            self.drone.send_control_command("{} {}".format('up' if u_d_distance >=0 else 'down', abs(u_d_distance)),timeout = 40)
            self.drone.send_rc_control(0,0,0,0)
        
        self.z = int(self.current_waypoint["z"])

        self.hover()
        ix = self.upload_current_frame()
        self.upload_fire_details(ix)

    def move_auto(self):
        l_r_distance = int(self.current_waypoint["x"]) - int(self.prev_waypoint["x"]) 
        b_f_distance = int(self.current_waypoint["y"]) - int(self.prev_waypoint["y"])
        u_d_distance = int(self.current_waypoint["z"]) - int(self.prev_waypoint["z"])

        self.drone.go_xyz_speed(b_f_distance, -l_r_distance, u_d_distance, 30)

        self.x = int(self.current_waypoint["x"])
        self.y = int(self.current_waypoint["y"])
        self.z = int(self.current_waypoint["z"])


    def hover(self):
        '''
        makes the drone hover in place
        '''
        self.drone.send_rc_control(0,0,0,0)
    
    # Streaming and Image Processing Functions
    def stream_current_frame(self):
        # Streams the current frame the drone's camera has captured
        frame = self.drone.get_frame_read().frame

        cv2.imshow("Stream", frame)
    

    def upload_current_frame(self):
        '''
        Uploads the current frame the drone's camera has captured
        with relevant meta data
        '''

        frame = self.drone.get_frame_read().frame

        # STORES IMAGE TO LOCAL DATABASE
        # WITH METADATA
        num_images = len(glob("./test_images/*"))

        frame = cv2.flip(frame, 0)

        # stores image locally
        cv2.imwrite(f'image_folder/image_waypoint_{self.image_no}.png', frame)
        cv2.imwrite(f'image_local/image_waypoint_{self.image_no}.png', frame)
        self.image_no += 1

        # crops image
        # image_processing.crop(f'test_images/image_waypoint_{num_images}.png',0,600,0,900)

        # processes image
        # image_processing.detect_fire(f'test_images/image_waypoint_{num_images}.png', 
        #                             f'test_images_results/image_waypoint_{num_images}_results.png')

        # stores path to image and other relevant metadata in the database
        self.imageCollection.insert_one(
            {
                "path": f'./image_folder/image_waypoint_{num_images}.png',
                "location": (round(self.x),round(self.y),round(self.z)),
                "time": "to be implemented"
            }
        )

        return num_images

    def upload_fire_details(self, image_num):
        fire_list = detect_fire( f'./image_local/image_waypoint_{self.image_no-1}.png', f'./image_local/image_waypoint_{self.image_no-1}_results.png')
        fires = calc_location_fire((self.x, self.y, self.z), fire_list)
        fire_details = {"location" : {"x": self.x, "y": self.y, "z": self.z},
                        "fires" : fires,
                        "time" : datetime.now().strftime("%H:%M:%S")
                        }
        print("fire ", self.fire_no, " ",fire_details)

        with open(f'./fire_folder/fire_data_{self.fire_no}.json', 'w') as f:
            json.dump(fire_details, f)
        self.fire_no += 1


    # Get functions
    def get_waypoints(self):
        # Returns all of the drone's waypoints
        return self.waypoints
    

    def get_current_position(self):
        # Returns the current x y z position of the drone
        return (self.x, self.y, self.z)

    def get_current_waypoint(self):
        # Returns the current waypoint of the drone
        return self.current_waypoint
    

    # def get_speed(self):
    #     # Returns the speed of the drone
    #     return self.lspeed

        

                        



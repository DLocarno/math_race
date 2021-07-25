
import pygame
import os
import math
import random

from race.GameObject import ImageObject
from race import CollisionManager

class NpcCar(ImageObject):
    
    def __init__(self, npc_attributes, game_objects):
        # For each new NPC, select an image filename at random from the list of avail images
        random_image = random.randint(0, len(npc_attributes["IMAGE_FILES"])-1)
        image_file = npc_attributes["IMAGE_FILES"][random_image]
        # Retrieve the start coords via the level data for the NPC being created
        coords = (npc_attributes["NPC_START_COORDS"][0]) # Get start coords from front of list (x,y,angle)
        # After start coords for this npc instance are retreived, remove them
        npc_attributes["NPC_START_COORDS"].pop(0)
        # Init the parent class, passing the formatted params
        super().__init__(coords, image_file) # pass x,y,deg coords and image file
        
        # Init the NPC's attributes randomly based on npc attribute range values specified in main.py
        self.max_speed = round(random.uniform(npc_attributes["MAX_SPEED"][0], npc_attributes["MAX_SPEED"][1]), 2)
        self.handling = round(random.uniform(npc_attributes["HANDLING"][0], npc_attributes["HANDLING"][1]), 2)
        self.accel = round(random.uniform(npc_attributes["ACCEL"][0], npc_attributes["ACCEL"][1]), 3)
        self.deceleration = npc_attributes["DECELERATION"]
        self.npc_points = npc_attributes["NPC_POINTS"]
        
        self.game_objects = game_objects
        
        self.lap_count = 0
        self.current_waypoint = None
        self.last_waypoint = 0
        self.waypoint_counter = 0
        # Load all the waypoints for the npc being initialized for the current level
        self.waypoints = self.generate_waypoints()
        self.angle = coords[2]
        self.throttle = False
        self.throttle_start_time = 0
        self.throttle_time = 0
        self.distance = 0
        self.previous_distance = 0
        
    def init_collision_manager(self):
        self.collision_manager = CollisionManager.CollisionManager(self, self.game_objects)
 
    def generate_waypoints(self):
        waypoints = []
        for each in self.npc_points:
            random_point = random.randint(0, len(each) -1) # For each series of points, randomly select a way point (x,y)
            waypoints.append(each[random_point])
        self.last_waypoint = len(waypoints) # Total number of waypoints assigned to waypoint_last
        self.current_waypoint = waypoints[0] # Init first waypoint
        self.waypoint_counter += 1
        return waypoints
              
    def update(self):
        self.collision_manager.get_collisions()
        self.determine_waypoint()       # Determine the next place to go
        self.generate_move_signals()    # Generate the needed control singals to get there

        # Checks whether to move the car based on either a collision or key inputs
        if self.collision_level == True:
            self.collision_count = self.collision_constant_level
            self.collision_counter = self.collision_count[0] # Start the collision counter for level coll
        elif self.collision_player == True:
            self.collision_count = self.collision_constant_player
            self.collision_counter = self.collision_count[0] # Start the collision counter for level coll
        if self.collision_counter > 0:
            self.move_collision()
        else:
            self.move()
        # updates car rect coords based on new calcualtion
        self.rect.x = self.x
        self.rect.y = self.y   
    
    def move_collision(self):
        if self.collision_right == True and self.collision_down == True:
            self.x = self.x - self.collision_counter / self.collision_count[1]
            self.y = self.y - self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_right == True and self.collision_up == True:
            self.x = self.x - self.collision_counter / self.collision_count[1]
            self.y = self.y + self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_left == True and self.collision_down == True:
            self.x = self.x + self.collision_counter / self.collision_count[1]
            self.y = self.y - self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_left == True and self.collision_up == True:
            self.x = self.x + self.collision_counter / self.collision_count[1]
            self.y = self.y + self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_right == True:
            self.x = self.x - self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_left == True:
            self.x = self.x + self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_up == True:
            self.y = self.y + self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
        if self.collision_down == True:
            self.y = self.y - self.collision_counter / self.collision_count[1]
            self.collision_counter -= 1
            
        
    # Updates its x,y coords to move npc car, accounts for turning
    def move(self):
        self.calc_distance()            # Calc distance change (speed)
        # Account for turning and set x and y coords
        rad = (self.angle * math.pi) / 180
        self.x = self.x + self.distance * math.cos(rad)
        self.y = self.y + self.distance * math.sin(rad)
    
    # Determine if the current waypoint has been reached, if so,
    # load the next waypoint
    def determine_waypoint(self):
        x = self.current_waypoint[0]
        y = self.current_waypoint[1]
        # If NPC is within 500 pixels of its x and y waypoints, select the next point to control to
        if abs(x - self.x) < 500 and abs(y - self.y) < 500:
            self.current_waypoint = self.waypoints[self.waypoint_counter]
            self.waypoint_counter += 1
            # Check to see if we need to restart at first waypoint
            if self.waypoint_counter >= self.last_waypoint:
                self.waypoint_counter = 0
                
    # Generate the NPC's move singals based on the
    # current waypoint its trying to get to    
    def generate_move_signals(self):        
        if self.collision_level == True:    # If collision is with level
            self.throttle = False           
            self.previous_distance = 0      # Speed = 0
            self.throttle_start_time = 0    # Restart acceleration timer
            self.throttle_time = 0
            return None
        elif self.collision_player == True: # Keep throttle if collision is with player
            self.throttle = False
            return None
        else:
            self.throttle = True       # Throttle always on if move() was called
        # only allow turning if vehicle is currently in motion
        if self.previous_distance > 0:
            # Handling improves as vehicle speed increases
            handling = self.handling * (self.previous_distance / self.max_speed)
            # Assign x,y coords of current waypoint to local vars
            x = self.current_waypoint[0]
            y = self.current_waypoint[1]
            # Calculates the orientation angle of where the car SHOULD be if it was 
            # on-track to the waypoint
            ang = math.atan2(y - self.y, x - self.x) 
            deg = math.degrees(ang) % 360   # Convert to degrees and normalize from 0 to 360
            # Side note-- this bit gave me the biggest difficulty in the whole game's design!
            # 'diff' used to determine "shortest" turning distance (ie. left or right turn shortest)
            # to get to the waypoint angle relative to the NPC's current orientation
            diff = ((self.angle - deg + 180) % 360) - 180   # Oh no, its.....MATH!!!               
            # "deadband" of 1 degree used so the NPC car doesn't "jitter" from right to
            # left as it constantly attempts to control to too precise of an angle
            deadband = abs(diff)
            # Finally, we can update the left or right turn signal.
            if diff < 0 and deadband > 1:
                self.angle += 1 * self.handling
            elif diff > 0 and deadband > 1:
                self.angle -= 1 * self.handling
        # normalize (updated) car angle between 0 and 360 degrees
        self.angle = self.angle % 360           
        self.rotate_image() # Method call to update the car's image with new rotation

        # Calculate how long throttle has been held down--used for acceleration of vehicle
        # When throttle is first pressed, get the current time
        if self.throttle and self.throttle_start_time == 0: 
            self.throttle_start_time = pygame.time.get_ticks()
        # Throttle is still down since last iteration
        elif self.throttle:
            self.throttle_time = pygame.time.get_ticks() - self.throttle_start_time # current time - initial
            self.throttle_time = self.throttle_time / 1000 # convert from ms to seconds
        # Throttle not pressed, reset timers
        else:
            self.throttle_start_time = 0
            self.throttle_time = 0
    
    def rotate_image(self):
        image_angle = self.angle
        image_angle = str(int(image_angle)) # truncate the angle and convert to string to call the right filename
        # UPDATE CAR MASK
        self.image = pygame.image.load(self.image_basename + "_" + image_angle + ".png")
        self.rect = self.image.get_rect()
        self.image.set_colorkey("white")
        self.image.convert_alpha()
        self.car_mask = pygame.mask.from_surface(self.image)
    
    def calc_distance(self):
        if self.throttle_time == 0: # No brake--gently coast until speed is 0
                self.distance = max(0, self.previous_distance - self.deceleration)      
        # calc distance based on acceleration constant and time throttle has been held
        else:
            self.distance = self.previous_distance + self.accel * self.throttle_time
        # Prevents acceleration past player's maximum speed constant
        if self.distance > self.max_speed:
            self.distance = self.max_speed
            
        self.previous_distance = self.distance    # update distance to move (ie. speed)
    
        
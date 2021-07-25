# required modules
import pygame
import os
import math

from race.GameObject import ImageObject
from race import CollisionManager

# Inits and controls player's car object.
# Inherets some additional attributes from ImageObject parent class  
class PlayerCar(ImageObject):
    
    def __init__(self, player_attributes, key_states, game_objects):
        # Get image_file from attributes argument
        image_file = player_attributes["IMAGE_FILE"]
        super().__init__(player_attributes["START_COORDS"], image_file) # Init ImageObject parent class     
        
        # Init player's car attribute stats, key states, and reference to other game_objects
        self.max_speed = player_attributes["MAX_SPEED"] / 10
        self.accel = player_attributes["ACCEL"] / 100
        self.handling = player_attributes["HANDLING"]
        self.deceleration = player_attributes["DECELERATION"]
        self.e_brake_deceleration = player_attributes["E_BRAKE_DECEL"]
        self.e_brake_handling = player_attributes["E_BRAKE_HANDLING"]
        self.health = player_attributes["HEALTH"]
        self.boost_count = player_attributes["BOOST"]
        self.keys = key_states
        self.game_objects = game_objects
        
        self.lap_count = 0
        # Player's car control state variables. Times are used for acceleration calcs
        self.e_brake = False
        self.throttle = False
        self.boost = False
        self.throttle_start_time = 0
        self.throttle_time = 0
        self.boost_start_time = 0
        self.boost_time = 0
        self.distance = 0
        self.previous_distance = 0

    def init_collision_manager(self):
        self.collision_manager = CollisionManager.CollisionManager(self, self.game_objects)
    
    # Update all required data -- including 
    # Gets collisions via collison mngr, gets updated key inputs and clock info, etc.
    # Then make calls to functions to calculate how to move the car
    def update(self):
        self.collision_manager.get_collisions() # Gets collisions
        self.set_signals()
        # Checks whether to move the car based on either a collision or key inputs
        if self.collision_level == True:
            self.collision_count = self.collision_constant_level
            self.collision_counter = self.collision_count[0]    # Start the collision counter
        elif self.collision_player == True:
            self.collision_count = self.collision_constant_player
            self.collision_counter = self.collision_count[0]
        if self.collision_counter > 0:
            self.move_collision()
        else:
            self.move()
           
        
        # updates car rect coords based on new calcualtion
        self.rect.x = self.x
        self.rect.y = self.y
    
    # Determines how the car should be moved based on where the collision
    # on the car occured (as determined by the collision manager)
    def move_collision(self):
        #print(self.collision_left, self.collision_right, self.collision_down, self.collision_up)
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
        
        
        
    # Moves the car to the new calculated distance based on 
    # speed and turning calculations
    def move(self):
        # Performs distance to move calc (updates self.distance)
        self.calc_distance() 
        # convert the turn angle into radians
        rad = (self.angle * math.pi) / 180
        # Accounts for turning and calculates new x and y coordinates
        self.x = self.x + self.distance * math.cos(rad)
        self.y = self.y + self.distance * math.sin(rad)
        
    # Gets user key inputs and sets car's control signals
    def set_signals(self):
        if self.collision_level == True:    # If collsion with level--
            self.previous_distance = 0      # Set speed to 0 and reset throttle (accel time)
            self.throttle_start_time = 0
        elif self.collision_player == True:
            self.previous_distance *= .15    # If collision with player, momentarily reduce speed to 15%
        if self.keys["left"] == True:       # get turn angle & rotate left
            self.calc_turn_angle("L")
            self.rotate_image()
        if self.keys["right"] == True:        # get turn angle & rotate right
            self.calc_turn_angle("R")
            self.rotate_image()
        if self.keys["forward"] == True:    # Accelerate 
            self.throttle = True
        else:
            self.throttle = False           # Decelerate
        if self.keys["e_brake"] == True:    # E-Brake signal ON, reset throttle acceleration timer
            self.e_brake = True
            self.throttle_start_time = 0
            self.throttle_time = 0
        else:
            self.e_brake = False            # Turn e-brake off if key isn't pressed
        if self.keys["boost"] == True:      # Boost
            self.boost = True

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
                
        # If boost, 40% max speed and 400% accel increase
        if self.boost == True and self.boost_count > 0 and self.boost_start_time == 0:
            self.boost_start_time = pygame.time.get_ticks()
            self.max_speed = self.max_speed * 1.4
            self.accel = self.accel * 4
            self.boost_count -= 1
        # Boost timer already initiated, get elapsed boost time
        elif self.boost_start_time > 0:
            self.boost_time = (pygame.time.get_ticks() - self.boost_start_time) // 1000
        # After 4 seconds boost ends - reduce max_speed value to original, reset timers
        if self.boost_time >= 4:
            self.max_speed = self.max_speed / 1.4
            self.accel = self.accel / 4
            self.boost_start_time = 0
            self.boost_time = 0
            self.boost = False
 
    def calc_turn_angle(self, direction):
        # Only allow turning if vehicle is still in motion
        if self.previous_distance > 0:
            # Adjust handling based on handling constant and current_speed
            #(faster speed = improved handling)
            handling = self.handling * (self.previous_distance / self.max_speed) 
            # Generate handling boost if e_braking WITHOUT accelerator (4 considered ideal)
            if self.e_brake == True and self.throttle == False:
                handling = handling + (self.e_brake_handling - handling)
            # Adjust angle based on the handling calc
            if direction == "L": # Turn left
                self.angle -= 1 * handling
            else:                # Turn right
                self.angle += 1 * handling
        # normalize angle between 0 and 360 degrees
        self.angle = self.angle % 360
        
    # Updates player's car image file (orientation) according to new turn angle
    def rotate_image(self):
        image_angle = self.angle
        image_angle = str(int(image_angle)) # truncate the angle and convert to string to call the right filename
        
        # UPDATE CAR MASK
        self.image = pygame.image.load(self.image_basename + "_" + image_angle + ".png")
        self.rect = self.image.get_rect()
        self.image.set_colorkey("white")
        self.image.convert_alpha()
        self.car_mask = pygame.mask.from_surface(self.image)
    
    # Calculates cars new distance (speed) on the map based on acceleration and time
    def calc_distance(self):
        # if no throttle, decelerate player
        if self.throttle_time == 0 and self.e_brake == False: # No brake--gently coast until speed is 0
                self.distance = max(0, self.previous_distance - self.deceleration)
        elif self.e_brake == True: # if e_breaking, use E_BRAKE_DECELERATION instead
                self.distance = max(0, self.previous_distance - self.e_brake_deceleration)        
        # Else, player is accelerating (self.throttle == True)
        # calc distance based on acceleration constant and time throttle has been held
        else:
            self.distance = self.previous_distance + self.accel * self.throttle_time
        # Prevents acceleration past player's maximum speed constant
        if self.distance > self.max_speed:
            self.distance = self.max_speed
            
        self.previous_distance = self.distance    # update distance to move (ie. speed)
        # Prints "speed" representation
        #print(self.distance)

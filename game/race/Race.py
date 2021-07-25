# required modules
import pygame
import sys
import time

# All classes for Race portion of the game:
from race import GameObject
from race import PlayerView
from race import Level
from race import FinishLine
from race import PlayerCar
from race import NpcCar
        
    
class Race:

    def __init__(self, game):
        self.game = game
        # Init all necc game variables from Main class
        self.screen = game.screen
        self.clock = game.clock
        self.FPS = game.FPS
        self.display = game.display
        self.screen_rect = self.screen.get_rect()
        
        self.player_selection = game.player_selection
        self.level_selection = game.level_selection
        self.npc_car_images = game.npc_car_images
        
        # Call the game's race loop
        self.race_loop()
        
        
    
    # Initializes imported player attributes, as determined by a previous game sequence.  If, for some reason,
    # these attributes were never set/initialized, default values are initialized instead.
    def init_player_attributes(self):
        
        if self.game.player_attributes != None:
            # Init some default (non-variable) attribute values
            self.player_attributes = {"IMAGE_FILE": self.player_selection, # sprite image file
                                      "DECELERATION": .02, # .05
                                      "E_BRAKE_DECEL": .07, # .175
                                      "E_BRAKE_HANDLING": 2.5, # 4.25
                                      "START_COORDS": (self.level.player_start_coords[0], self.level.player_start_coords[1], self.level.player_start_coords[2])} # x,y,deg coords
        
            # Init remaining (variable) attributes from previous sequence, as determined by player
            for attribute, value in self.game.player_attributes.items():
                self.player_attributes[attribute] = value
                
        else:
            # Set all attributes to default (hard-coded) values, instead
            self.player_attributes = {"IMAGE_FILE": self.player_selection, # sprite image file
                                      "MAX_SPEED": 150, # Range 200 -350
                                      "ACCEL": 1,      # Range .5 - 7
                                      "HANDLING": 2, # Range 1.5 - 3
                                      "DECELERATION": .02, # .05
                                      "E_BRAKE_DECEL": .07, # .175
                                      "E_BRAKE_HANDLING": 2.5, # 4.25
                                      "START_COORDS": (self.level.player_start_coords[0], self.level.player_start_coords[1], self.level.player_start_coords[2])} # x,y,deg coords

    # Initializes NPC attributes with a low and high range.  Range helps establish randomness between NPCs
    # To make npc's more difficult, increase attribute values &/or narrow the value range
    def init_npc_attributes(self):
        self.npc_attributes = {"MAX_SPEED": (9,12),
                               "ACCEL": (.004, .05),     
                               "HANDLING": (.5, 1),  
                               "DECELERATION": .025,
                               "IMAGE_FILES": self.npc_car_images,
                               "NPCS": self.level.npcs,
                               "NPC_START_COORDS": self.level.npc_start_coords,
                               "NPC_POINTS": self.level.npc_points}
    
    # Update objects - Makes obj method calls to detect each of
    # their collision status', calculate their next movements, etc.
    def update(self):    
        self.level.update()
        self.player_car.update()
        for car in self.npc_cars:
            car.update()
        self.finish_line.update()
        self.player.update_viewport()
    
    # Makes call to player's viewport to finalize the drawing of everything to the screen
    def draw(self):
        self.player.display_viewport() # Draws map w/all actors to display
        pygame.display.update() # After all draws, update (print) the game's display
    
    # Inits all race objects and then starts the race loop
    def race_loop(self):
        # Init a dictionary to store all in-game (race) objects
        self.game_objects = {}
        # Init level and get critical level data from level's init .txt file to init all additional objects
        self.level = Level.Level(self.level_selection)     
        # Init race finish line
        self.finish_line = FinishLine.FinishLine(self.level, self.game_objects, self.game)    
        # Init the loaded attributes for race objects
        self.init_player_attributes()
        self.init_npc_attributes()
        # Init player car
        self.player_car = PlayerCar.PlayerCar(self.player_attributes, self.game.key_state, self.game_objects)
        # Init npc car(s)
        self.npc_cars = []
        for i in range(0, self.npc_attributes["NPCS"], 1):
            self.npc_cars.append(NpcCar.NpcCar(self.npc_attributes, self.game_objects))
        # Update dict w/all game objects for their reference
        self.game_objects.update({"level": self.level, "finish_line": self.finish_line, "player_car": self.player_car, "npc_cars": self.npc_cars})
        # Now with all game objects we needed created, init each car objects' collision manager
        self.player_car.init_collision_manager()
        for car in self.npc_cars:
            car.init_collision_manager()
        # Init the player's viewport
        self.player = PlayerView.PlayerView(self.screen, self.game_objects)
        
        # The race loop
        while self.game.running:
            
            self.game.get_events()  # Update key inputs from Main class      
            self.update()
            self.draw()
            self.clock.tick(self.FPS) # Ensures framerate constant is maintained
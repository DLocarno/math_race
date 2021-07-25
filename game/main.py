# required modules
import pygame
import os
import sys
import time

# Import Classes for different parts of the game
import Title
import Intro
import ImproveAttributes
from race import Race
from math_game import MathGame
        
# The Main class inits the entire game with default game variables, such as the FPS, 
# screen height and width, etc.  It also initializes the player's key input bindings and states,
# and, finally moves the game from one state to another.  For example, it starts the game at its
# title sequence, and when that's complete, it then moves to the next game sequence.
class Main:

    def __init__(self):
        self.name = "Math Race"
        self.FPS = 120  # 120 FPS Reccommended, 60 FPS secondary option1
        self.WIDTH = 1400
        self.HEIGHT = 900
        self.colors = {"red": (255,0,0), "green": (0,128,0), "blue": (0,0,255), "black": (0,0,0), "white": (255,255,255), 
                        "yellow": (255,255,0), "darkgreen": (0,100,0), "skyblue": (135,206,235), "snow": (255, 250, 250),
                        "silver": (192,192,192), "lime": (0,255,0), "khaki": (240,230,140), "orange": (255,165,0), "paper": (242,242,242)}
        self.background_color = self.colors["white"]
        self.running = True
        
        pygame.init()
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.caption = pygame.display.set_caption(self.name)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        
        # Init variables to store critical game/player information to be shared 
        # across different game states/sequences -- Do not need to modify
        self.player_selection = None
        self.level_selection = None
        self.player_attributes = None
        self.player_score = 0
        self.player_attributes = None
        
        # Methods calls for more initializing
        self.setup_background()
        self.init_key_bindings()
        self.get_image_files()
        
        self.init_title_screen()    # Game is setup, go to the title screen
    
    def get_image_files(self):
        self.car_image_directory = "race/car_sprite_images/"
        self.car_images = ["blue_car.png", "green_car.png", "red_car.png", "orange_car.png", "yellow_car.png", "purple_car.png", "navy_car.png", "pink_car.png", "white_car.png", "black_car.png", "forest_car.png"]
        
        self.level_image_directory = "race/track_images/"
        self.level_images = []
        
        for image_file in os.listdir(self.level_image_directory):
            if image_file.endswith(".png"):
                self.level_images.append(image_file)

    def setup_background(self):
        self.background = pygame.Surface(self.display.get_size())
        self.background = self.background.convert()
        self.background.fill(self.background_color)
        self.display.blit(self.background, (0,0))
        
    def init_key_bindings(self):
        
        self.key = {"left": pygame.K_LEFT,
                    "right": pygame.K_RIGHT,
                    "up": pygame.K_UP,
                    "down": pygame.K_DOWN,
                    "escape": pygame.K_ESCAPE,
                    "enter": pygame.K_RETURN,
                    "forward": pygame.K_SPACE,
                    "e_brake": pygame.K_b,
                    "r_brake": pygame.K_r,
                    "boost": pygame.K_n}
        
        self.key_state = {"left": False,
                          "right": False,
                          "up": False,
                          "down": False,
                          "escape": False,
                          "enter": False,
                          "forward": False,
                          "e_brake": False,
                          "r_brake": False,
                          "boost": False,
                          "left_click": False}
                          
        # Checks for events (human player key inputs)                     
    def get_events(self):
        # Check for key input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
            if  event.type == pygame.KEYDOWN:
                if event.key == self.key["escape"]:
                    self.key_state["escape"] = True
                    self.running = False
                if event.key == self.key["enter"]:
                    self.key_state["enter"] = True
                if event.key == self.key["left"]:
                    self.key_state["left"] = True
                if event.key == self.key["right"]:
                    self.key_state["right"] = True
                if event.key == self.key["up"]:
                    self.key_state["up"] = True
                if event.key == self.key["down"]:
                    self.key_state["down"] = True
                if event.key == self.key["forward"]:
                   self.key_state["forward"] = True
                if event.key == self.key["e_brake"]:
                   self.key_state["e_brake"] = True
                if event.key == self.key["boost"]:
                    self.key_state["boost"] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.key_state["left_click"] = True
            
            if  event.type == pygame.KEYUP:
                if event.key == self.key["enter"]:
                    self.key_state["enter"] = False
                if event.key == self.key["left"]:
                    self.key_state["left"] = False
                if event.key == self.key["right"]:
                    self.key_state["right"] = False
                if event.key == self.key["up"]:
                    self.key_state["up"] = False
                if event.key == self.key["down"]:
                    self.key_state["down"] = False
                if event.key == self.key["forward"]:
                    self.key_state["forward"] = False
                if event.key == self.key["e_brake"]:
                    self.key_state["e_brake"] = False
                if event.key == self.key["boost"]:
                    self.key_state["boost"] = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.key_state["left_click"] = False
    
    def init_title_screen(self):
        Title.Title(self)
        self.npc_car_images = self.car_images
        self.npc_car_images = [self.car_image_directory + image for image in self.npc_car_images] # append the image directory to each image filename
        self.npc_car_images = [image for image in self.npc_car_images if image != self.player_selection] # Don't let npc's be same color as player's choice
        if self.running:
            self.init_intro_sequence()
        
    def init_intro_sequence(self):
        Intro.Intro(self)
        if self.running:
            self.init_math_game()
            
    def init_math_game(self):
        MathGame.MathGame(self)
        if self.running:
            self.init_attribute_sequence()
        
    def init_attribute_sequence(self):
        ImproveAttributes.ImproveAttributes(self)
        if self.running:
            self.init_race()
      
    def init_race(self):
        Race.Race(self)
    
# Init game object
if __name__ == '__main__':
    Main()

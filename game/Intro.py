import pygame
import os

import Parser

class Intro():
    
    def __init__(self, game):
        # Init attributes from Main game object
        self.game = game
        self.FPS = game.FPS
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        self.colors = game.colors
        self.background_color = self.colors["lime"]
        self.screen = game.screen
        self.player_car_filename = os.path.basename(game.player_selection)
    
        self.intro_running = True
        self.enter_down = False
        self.left_down = False
        self.right_down = False
        self.enter = False
        self.left = False
        self.right = False
        
        self.draw_objects = []
        self.textbox_font = pygame.font.SysFont("arial", 38)
        # Init objects
        self.text_parser = Parser.Parser()
        
        # Go to introduction
        self.init_intro()
    
    # Detect when keys are released instead of pushed
    def detect_key_up(self):
        if self.game.key_state["enter"]:
            self.enter = False
            self.enter_down = True
        if self.game.key_state["left"]:
            self.left = False
            self.left_down = True
        if self.game.key_state["right"]:
            self.right = False
            self.right_down = True
        
        if not self.game.key_state["enter"] and self.enter_down:
            self.enter_down = False
            self.enter = True
        if not self.game.key_state["left"] and self.left_down:
            self.left_down = False
            self.left = True
        if not self.game.key_state["right"] and self.right_down:
            self.right_down = False
            self.right = True
            
    def draw(self, objects):
        self.screen.fill(self.background_color)
        for each in objects:
            self.screen.blit(each[0],each[1])
        pygame.display.update()
        
    def generate_textbox(self, text_list):
        w = self.WIDTH
        h = self.HEIGHT
        linespace_height = 10
        # create a textbox
        textbox = pygame.Surface((int(.75 * w), int(.25 * h)))
        textbox.set_alpha(200) # Transparency level
        textbox.fill(self.colors["white"])
        # Create prompt
        prompt = pygame.font.SysFont("arial", 22).render("<Right arrow → next. Enter to Skip>", True, self.colors["black"])
        textbox.blit(prompt, (int(.7 * textbox.get_rect()[2]), int(.9 * textbox.get_rect()[3])))
        # Create and append the text from text_list
        for line in text_list:
            text = self.textbox_font.render(line, True, self.colors["black"])
            textbox.blit(text, (10, linespace_height))
            linespace_height += 38
        # Pair the object to be drawn with its placement coords
        textbox_obj = (textbox, (25, int(.75 * h)))
        return textbox_obj
        
     # Intro Sequence to Math Game   
    def init_intro(self):
        w = self.WIDTH
        h = self.HEIGHT
        # Load background image
        background_image = pygame.image.load("images/garage.png")
        background_image = pygame.transform.scale(background_image, (w, h))
        background_obj = (background_image, (0,0))
        # Load player car image
        car_image = pygame.image.load("images/" + self.player_car_filename)
        car_image = pygame.transform.scale(car_image, (int(.55 * w), int(.3* h)))
        car_obj = (car_image, (int(.25 * w),int(.6 * h)))
        # Load character image
        character_image = pygame.image.load("images/speedy.png")
        character_image.set_colorkey("white")
        character_image.convert_alpha()
        character_obj = (character_image, (int(.8 * w), int(.65 * h)))
        # Give parser object the intro transcript
        self.text_parser.load_transcript("intro_transcript.txt")
        text = self.text_parser.get_text()
        # Create the textbox object
        textbox_obj = self.generate_textbox(text)
        # Add objects to draw
        self.draw_objects.append(background_obj)
        self.draw_objects.append(car_obj)
        self.draw_objects.append(character_obj)
        self.draw_objects.append(textbox_obj)
        # Draw objects
        self.draw(self.draw_objects)
        
        # Intro sequence loop
        while self.game.running and self.intro_running:
            
            self.game.get_events()
            self.detect_key_up()
            if self.enter == True:
                break
            if self.right == True:
                text = self.text_parser.get_text()
                if not text:                        # At end of transcripts, exit sequence.
                    break
                self.draw_objects.pop()
                textbox_obj = self.generate_textbox(text)
                self.draw_objects.append(textbox_obj)
                self.draw(self.draw_objects)
                self.right = False
            self.game.clock.tick(self.FPS)

        
        
    
            
        
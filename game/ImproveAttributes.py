import pygame
import os

import Parser

class ImproveAttributes():
    
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
    
        # Retrieve Player Score
        self.player_score = game.player_score
        #self.player_score = 28000
        self.player_score_max = self.player_score
        self.SCORE_ADJ_FACTOR = 100
        
        self.text_sequence_over = False
        self.attribute_running = True
        self.enter_down = False
        self.left_down = False
        self.right_down = False
        self.down_down = False
        self.up_down = False
        self.enter = False
        self.left = False
        self.right = False
        self.down = False
        self.up = False
        self.right_key_start = 0
        self.left_key_start = 0
        self.right_key_time = 0
        self.left_key_time = 0
        self.exit_prompt = False
        
        self.draw_objects = []
        self.textbox_font = pygame.font.SysFont("arial", 38)
        self.text_parser = Parser.Parser()
        
        # Go to introduction
        self.init_base_attributes()
        self.init_background()
        self.init_text_sequence()
        self.game_loop()
    
    def init_base_attributes(self):
        # Init variable used to keep track of active attribute window
        self.active_attribute = 1
    
        # Maximum possible attribute values
        MAX_SPEED = 150
        MAX_ACCEL = 7
        MAX_HANDLING = 2.25
        MAX_HEALTH = 200
        MAX_BOOST = 10
        # Base attribute values (initial values)
        BASE_SPEED = 50
        BASE_ACCEL = .2
        BASE_HANDLING = 1
        BASE_HEALTH = 100
        BASE_BOOST = 0
        # Increment amount values
        speed_i = MAX_SPEED / 100
        accel_i = MAX_ACCEL / 100
        handling_i = MAX_HANDLING / 100
        health_i = MAX_HEALTH / 100
        boost_i = 1
        # Init player adjusted values
        speed = BASE_SPEED 
        accel = BASE_ACCEL 
        handling = BASE_HANDLING 
        health = BASE_HEALTH 
        boost = BASE_BOOST   
        # Accesible dictionary
        self.attribute_vals = {"Health": [BASE_HEALTH, MAX_HEALTH, health_i, health],
                           "Acceleration": [BASE_ACCEL, MAX_ACCEL, accel_i, accel],
                           "Handling": [BASE_HANDLING, MAX_HANDLING, handling_i, handling],
                           "Speed": [BASE_SPEED, MAX_SPEED, speed_i, speed],
                           "Boost": [BASE_BOOST, MAX_BOOST, boost_i, boost] }
        
    
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
        if self.game.key_state["down"]:
            self.down = False
            self.down_down = True
        if self.game.key_state["up"]:
            self.up = False
            self.up_down = True
        
        if not self.game.key_state["enter"] and self.enter_down:
            self.enter_down = False
            self.enter = True
        if not self.game.key_state["left"] and self.left_down:
            self.left_down = False
            self.left = True
        if not self.game.key_state["right"] and self.right_down:
            self.right_down = False
            self.right = True
        if not self.game.key_state["down"] and self.down_down:
            self.down_down = False
            self.down = True
        if not self.game.key_state["up"] and self.up_down:
            self.up_down = False
            self.up = True
            
    def draw(self, objects):
        # If there's nothing new to draw, exit method 
        if not objects:
            return
        # Otherwise draw all objects
        for each in objects:
            self.screen.blit(each[0],each[1])
        # Remove each object after drawn
        self.draw_objects = []
        # Update the screen
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
        
    def init_background(self):
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
        # Add objects to draw
        self.draw_objects.append(background_obj)
        self.draw_objects.append(car_obj)
        self.draw_objects.append(character_obj)

     # Intro Sequence to Math Game   
    def init_text_sequence(self):
        w = self.WIDTH
        h = self.HEIGHT
        # Give parser object the intro transcript
        self.text_parser.load_transcript("attribute_transcript.txt")
        text = self.text_parser.get_text()
        # Create the textbox object
        textbox_obj = self.generate_textbox(text)
        # Add objects to draw
        self.draw_objects.append(textbox_obj)
        
    # Navigate text sequence. Once end of transcript is reached,
    # attribute sequence is init'd
    def update_text(self):
        # If user pressed right key, scroll textbox
        if self.right == True:
            # Remove previous textbox by redrawing background
            self.init_background()
            # Now redraw textbox with new text
            text = self.text_parser.get_text()
            textbox_obj = self.generate_textbox(text)
            self.draw_objects.append(textbox_obj)
            self.right = False
            # If transcript ends, end this sequence, and go to next
            if not text:
                self.text_sequence_over = True
                self.update_attributes()
        # Ends text sequence if "enter" is pressed and goes to next
        elif self.enter == True:
            self.text_sequence_over = True
            self.enter = False
            self.update_attributes()
            return
        # No user input since last call--do nothing
        else:
            return
            
    def update_attributes(self):
        # Clear all draw objects and re-add background to draw list
        self.init_background()

        # Declare vars to build player score and attribute interface windows
        w = self.WIDTH
        h = self.HEIGHT
        width = w * .25
        height = h * .05
        x = .045 * w
        y = .05 * h
        xpad = .05 * w
        ypad = .05 * h
        yspace = .11 * h
        red = self.colors["red"]
        black = self.colors["black"]
        white = self.colors["white"]
        blue = self.colors["blue"]
        score_font = pygame.font.SysFont("arial", int(h * .075), bold=True)
        lg_font = pygame.font.SysFont("arial", int(h * .05), bold=True)
        sm_font = pygame.font.SysFont("arial", int(h * .03), bold=True)
        
        # Construct player score window
        score_box = pygame.Surface((w * .45, h * .1))
        score_box.fill(white)
        #score_box.set_alpha(200)
        score_box_obj = (score_box, (w * .5, y))
        score_text = score_font.render("Power-up Points: " + str(self.player_score), True, red)
        score_text_obj = (score_text, (w * .5, y))
        self.draw_objects.append(score_box_obj)
        self.draw_objects.append(score_text_obj)
        
        # Construct background attribute window
        main_text = lg_font.render("Vehicle Attributes", True, black)
        text_rect = main_text.get_rect()
        center_text = (width - text_rect.w) // 2
        main_text_obj = (main_text, (x + center_text, y))
        main_box = pygame.Surface((w * .26, h * .6))
        main_box.fill(white)
        main_box.set_alpha(200)
        main_box_obj = (main_box, (x, y))
        self.draw_objects.append(main_box_obj)
        self.draw_objects.append(main_text_obj)
        
        # Construct individual attribute boxes
        self.attributes = ["Health", "Acceleration", "Speed", "Handling", "Boost"]
        for i in range(1,len(self.attributes)+1, 1):
            # Change color of active attribute window to blue
            if self.active_attribute == i:
                color = blue
            else:
                color = black
            # Construct attribute name text objects
            text = sm_font.render("←   " + self.attributes[i-1] + "   →", True, color)
            text_rect = text.get_rect()
            center_text = (width - text_rect.w) // 2
            text_obj = (text, (x + center_text, yspace * i))
            # Construct attribute box
            attrib_box = pygame.Surface((width, height))
            attrib_box.fill(black)
            attrib_box_obj = (attrib_box, (xpad, ypad + yspace * i))
            # Construct attribute status bars - "width" var is equal to 100%
            # Uses the current iteration attribute value stored in attribute dictionary
            # ie.(current attribute val / max attribute val) * width of attribute box) correlates to attribute bar size to display
            attrib_bar = pygame.Surface(((self.attribute_vals[self.attributes[i-1]][3] / self.attribute_vals[self.attributes[i-1]][1]) * width, height))
            attrib_bar.fill(red)
            attrib_bar_obj = (attrib_bar, (xpad, ypad + yspace * i))
            # Add all objects to draw list
            self.draw_objects.append(text_obj)
            self.draw_objects.append(attrib_box_obj)
            self.draw_objects.append(attrib_bar_obj)

    # Checks player key inputs and makes attribute adjustments accordingly
    # After attribute adjustments, calls update_attributes in order to
    # re-display on screen
    def check_attribute_inputs(self):
        # Checks for Enter key input, to confirm attribute 
        # Triggers exit prompt
        if self.enter == True and self.exit_prompt == False:
            self.enter = False
            self.prompt_confirmation(0)
        
        # If exit prompt was triggered -- Get confirmation and end sequence
        # While prompt is still open, skip everytrhing else
        if self.exit_prompt:
            if self.right == True and self.exit_selection == 1:
                self.right = False
                self.left = False
                self.prompt_confirmation(0)
            elif self.left == True and self.exit_selection == 0:
                self.left = False
                self.right = False
                self.prompt_confirmation(1)
            elif self.enter == True and self.exit_selection == 0:
                self.enter = False
                self.prompt_confirmation(2)
            elif self.enter == True and self.exit_selection == 1:
                self.enter = False
                self.prompt_confirmation(3)
            # Prompt is open, but no input given - skip everything else
            return
    
    
        # Checks for up / down menu attribute selection
        if self.down == True:
            self.active_attribute += 1
            if self.active_attribute > len(self.attributes):
                self.active_attribute = 1
            self.down = False
            self.update_attributes()
        if self.up == True:
            self.active_attribute -= 1
            if self.active_attribute < 1:
                self.active_attribute = len(self.attributes)
            self.up = False
            self.update_attributes()
        
        # Checks for right key attribute adjustment
        # Increase attribute point allocation the longer the key is held
        if self.right_down == True and self.right_key_start == 0:
            self.right_key_start = pygame.time.get_ticks()
        elif self.right_down == True and self.right_key_start > 0:
            self.right_key_time = (pygame.time.get_ticks() - self.right_key_start) // 1000
        else:
            self.right_key_start = 0
            self.right_key_time = 0
            
        # Checks for left key attribute adjustment
        # Decrease attribute point allocation the longer the key is held   
        if self.left_down == True and self.left_key_start == 0:
            self.left_key_start = pygame.time.get_ticks()
        elif self.left_down == True and self.left_key_start > 0:
            self.left_key_time = (pygame.time.get_ticks() - self.left_key_start) // 1000
        else:
            self.left_key_start = 0
            self.left_key_time = 0
        
        # Init variables for better clarity -- vals correspond to current (active) attribute
        base_val = self.attribute_vals[self.attributes[self.active_attribute-1]][0]
        max_val = self.attribute_vals[self.attributes[self.active_attribute-1]][1]
        increment_val = self.attribute_vals[self.attributes[self.active_attribute-1]][2]   
        curr_val = self.attribute_vals[self.attributes[self.active_attribute-1]][3]
        
        # If keydown, perform the attribute increase, point decrease, and then update screen
        if self.right_key_time != 0:
            # Ensure attributes don't exceed 100% of max value and avail points don't go below 0
            if (curr_val + increment_val * self.right_key_time) <= max_val and (self.player_score - self.SCORE_ADJ_FACTOR * self.right_key_time) >= 0:
                self.attribute_vals[self.attributes[self.active_attribute-1]][3] += increment_val * self.right_key_time
                self.player_score -= self.SCORE_ADJ_FACTOR * self.right_key_time
                self.update_attributes()
        # Else if single right key press
        elif self.right == True:
            self.left = False
            self.right = False
            if (curr_val + increment_val) <= max_val and (self.player_score - self.SCORE_ADJ_FACTOR) >= 0:
                self.attribute_vals[self.attributes[self.active_attribute-1]][3] += increment_val
                self.player_score -= self.SCORE_ADJ_FACTOR
                self.update_attributes()
            
        # If keydown, perform the attribute decrease, point increase, and then update screen        
        if self.left_key_time != 0:
            # Ensure attributes don't go below base values and avail points don't exceed original value
            if (curr_val - increment_val * self.left_key_time) >= base_val and (self.player_score + self.SCORE_ADJ_FACTOR * self.left_key_time) <= self.player_score_max:
                self.attribute_vals[self.attributes[self.active_attribute-1]][3] -= increment_val * self.left_key_time
                self.player_score += self.SCORE_ADJ_FACTOR * self.left_key_time
                self.update_attributes()
        # Else if single left key press
        elif self.left == True:
            self.right = False
            self.left = False
            if (curr_val - increment_val) >= base_val and (self.player_score + self.SCORE_ADJ_FACTOR) <= self.player_score_max:
                self.attribute_vals[self.attributes[self.active_attribute-1]][3] -= increment_val
                self.player_score += self.SCORE_ADJ_FACTOR
                self.update_attributes()
        
            
    def prompt_confirmation(self, selection):
        self.exit_prompt = True
        if selection == 0:
            self.exit_selection = 0
        if selection == 1:
            self.exit_selection = 1
        # Exit prompt
        if selection == 2:
            self.exit_prompt = False
            self.update_attributes()
            return
        # Export Attributes and quit sequence
        if selection == 3:
            self.end_sequence()
            return
 
        # Create Confirmation Window 
        w = self.WIDTH
        h = self.HEIGHT
        black = self.colors["black"]
        white = self.colors["white"]
        blue = self.colors["blue"]
        
        prompt_box = pygame.Surface((w * .38 ,h * .2))
        prompt_box.fill(white)
        prompt_box_obj = (prompt_box, (w * .38, h * .4))
        self.draw_objects.append(prompt_box_obj)
        # Prompt Text
        font = pygame.font.SysFont("arial", int(h * .05), bold=True)
        text = font.render("Are You Sure You're Done?", True, black)
        if selection == 0:
            yes = font.render("YES", True, black)
            no = font.render("NO", True, blue)
        if selection == 1:
            yes = font.render("YES", True, blue)
            no = font.render("NO", True, black)
        text_obj = (text, (w * .38, h * .4))
        yes_obj = (yes, (w * .38, h * .45))
        no_obj = (no, (w * .45, h * .45))
        self.draw_objects.append(text_obj)
        self.draw_objects.append(yes_obj)
        self.draw_objects.append(no_obj)
    
    # Exports player selected/set attributes to a shared "game" variable
    # from Main class object, and terminates this game sequence.
    def end_sequence(self):
        self.game.player_attributes = { "MAX_SPEED": self.attribute_vals["Speed"][3],
                                        "ACCEL": self.attribute_vals["Acceleration"][3], 
                                        "HANDLING": self.attribute_vals["Handling"][3],
                                        "HEALTH": self.attribute_vals["Health"][3],
                                        "BOOST": self.attribute_vals["Boost"][3] }

        self.attribute_running = False

                                    
        
            
    # Main game loop for this sequence
    def game_loop(self):
        while self.game.running and self.attribute_running:     
            self.game.get_events()
            self.detect_key_up()
            if self.text_sequence_over == False:
                self.update_text()
            else:   # Text/Intro sequence ended previously
                self.check_attribute_inputs()
            self.draw(self.draw_objects)
            self.game.clock.tick(self.FPS)

            
        
        
    
            
        
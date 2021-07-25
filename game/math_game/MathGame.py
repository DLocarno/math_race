import pygame
from math_game.question_generator import generate_question


class MathGame():

    def __init__(self, game):
        self.game = game
        self.FPS = game.FPS
        self.WIDTH = game.WIDTH
        self.HEIGHT = game.HEIGHT
        self.colors = game.colors
        self.background_color = self.colors["white"]
        self.screen = game.screen
        self.math_running = True
        self.draw_objects = []
        self.left_click = False
        self.player_score = 0
        self.score_mult_count = 1
        self.CORRECT_ANS_POINTS = 500 # Points for correct answer
        self.SCORE_MULT_MAX = 10 # Maximum score multiplier
        self.GAME_TIME = 3    # game time (in minutes), Must be an integer
          
        self.screen.fill(self.background_color)
        self.update_game_score()
        self.init_question_window()
        self.two_inputs = False
        self.init_answer_window()
        self.init_scratchpad()
        self.init_scratchpad_menu()
        self.init_numpad()
        # Init game start time
        self.prev_sec = 0
        self.start_time = pygame.time.get_ticks()
        # Start math game loop
        self.game_loop()
    
    def update_game_timer(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time)
        # Calc time left (must convert GAME_TIME from mins to milliseconds)
        time_left = self.GAME_TIME * 60000 - elapsed_time
        # Calculate seconds
        secs = (time_left // 1000) % 60
        # Calculate minutes
        mins = time_left // (60 * 1000)
        
        # Ensures timer is only drawn to screen once per second (less updates)
        if self.prev_sec != secs:
            self.prev_sec = secs
            
            # Create timer window
            width = self.WIDTH * .3
            height = self.HEIGHT * .06
            x = self.WIDTH * .4
            y = self.HEIGHT * .8
            color = self.colors["yellow"]
            if mins > 0:
                text_color = self.colors["black"]
            else:
                text_color = self.colors["red"]
            
            rect = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.screen, color, rect)
            font = pygame.font.SysFont("arial", self.HEIGHT // 17, bold=True)
            if secs > 9:
                timer = font.render("Time Left: " + str(mins) + ":" + str(secs), True, text_color)
            else:
                timer = font.render("Time Left: " + str(mins) + ":0" + str(secs), True, text_color)
            self.screen.blit(timer, rect)
                 
        # Ends the game when time expires
        if mins == 0 and secs == 0:
            self.end_game()
    
    # Extracts player's score to be used in next game sequence
    # then terminates current game sequence
    def end_game(self):
        self.game.player_score = self.player_score
        self.math_running = False
              
    # Creates the window area where each math question populated and
    # appends the math question to the created window area
    def init_question_window(self):
        width = self.WIDTH * .4
        height = self.HEIGHT * .25
        color = self.colors["white"]
        x = self.WIDTH * .01
        y = self.HEIGHT * .1
        # Create rect for question window
        rect = pygame.Rect(x, y, width, height)
        # Divide question window rect into horizontal sections to place question text
        fifth = rect.x + .2 * rect.width
        third = rect.x + .3 * rect.width
        half = rect.x + .5 * rect.width
        three_fifth = rect.x + .6 * rect.width
        two_third = rect.x + .7 * rect.width
        # Divide question window rect into vertical sections to place question text
        top = rect.y + .2 * rect.height
        mid = rect.y + .4 * rect.height
        bot = rect.y + .6 * rect.height
        # Draw window Rect to screen
        pygame.draw.rect(self.screen, color, rect)
        # Calls generate_question function from question_generator.py
        self.question_type, self.question, self.correct_answer = generate_question()
        ##########################PRINTS EACH CORRECT ANSWER TO OUTPUT (for testing)##########################
        #print(self.correct_answer)
        ######################################################################################################
        font = pygame.font.SysFont("arial", self.HEIGHT // 12, bold=True)
        text_color = self.colors["black"]
        # Multiplication Problem Type
        if self.question_type == "mult":
            num1 = font.render(self.question[0], True, text_color)
            num2 = font.render(self.question[1], True, text_color)
            operator = font.render("x", True, text_color)
            
            num1_rect = num1.get_rect()
            num2_rect = num2.get_rect()
            op_rect = operator.get_rect()
            
            num1_rect.center = (third, mid)
            op_rect.center = (half, mid)
            num2_rect.center = (two_third, mid)
            
            # blit the question text
            self.screen.blit(num1, num1_rect)
            self.screen.blit(operator, op_rect)
            self.screen.blit(num2, num2_rect)
        # Division Problem Type
        if self.question_type == "div":
            num = font.render(self.question[0], True, text_color)
            den = font.render(self.question[1], True, text_color)
            operator = font.render("÷", True, text_color)
            
            num_rect = num.get_rect()
            den_rect = den.get_rect()
            op_rect = operator.get_rect()
            
            num_rect.center = (third, mid)
            op_rect.center = (half, mid)
            den_rect.center = (two_third, mid)
            
            # blit the question text
            self.screen.blit(num, num_rect)
            self.screen.blit(operator, op_rect)
            self.screen.blit(den, den_rect)
        # Adding Fraction Problem Type
        if self.question_type == "frac_add":
            fraction1 = pygame.Rect(fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            fraction2 = pygame.Rect(three_fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            pygame.draw.rect(self.screen, text_color, fraction1)
            pygame.draw.rect(self.screen, text_color, fraction2)
            
            num1 = font.render(self.question[0], True, text_color)
            den1 = font.render(self.question[1], True, text_color)
            num2 = font.render(self.question[2], True, text_color)
            den2 = font.render(self.question[3], True, text_color)
            operator = font.render("+", True, text_color)
            
            num1_rect = num1.get_rect()
            den1_rect = den1.get_rect()
            num2_rect = num2.get_rect()
            den2_rect = den2.get_rect()
            op_rect = operator.get_rect()
            
            num1_rect.center = (third,top)
            den1_rect.center = (third,bot)
            op_rect.center = (half, mid)
            num2_rect.center = (two_third,top)
            den2_rect.center = (two_third,bot)
            
            # blit the question text
            self.screen.blit(num1, num1_rect)
            self.screen.blit(num2, num2_rect)            
            self.screen.blit(operator, op_rect)
            self.screen.blit(den1, den1_rect)
            self.screen.blit(den2, den2_rect)    
        # Subtracting Fraction Problem Type
        if self.question_type == "frac_sub":
            fraction1 = pygame.Rect(fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            fraction2 = pygame.Rect(three_fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            pygame.draw.rect(self.screen, text_color, fraction1)
            pygame.draw.rect(self.screen, text_color, fraction2)
        
            num1 = font.render(self.question[0], True, text_color)
            den1 = font.render(self.question[1], True, text_color)
            num2 = font.render(self.question[2], True, text_color)
            den2 = font.render(self.question[3], True, text_color)
            operator = font.render("-", True, text_color)
            
            num1_rect = num1.get_rect()
            den1_rect = den1.get_rect()
            num2_rect = num2.get_rect()
            den2_rect = den2.get_rect()
            op_rect = operator.get_rect()
            
            num1_rect.center = (third,top)
            den1_rect.center = (third,bot)
            op_rect.center = (half, mid)
            num2_rect.center = (two_third,top)
            den2_rect.center = (two_third,bot)
            
            # blit the question text
            self.screen.blit(num1, num1_rect)
            self.screen.blit(num2, num2_rect)            
            self.screen.blit(operator, op_rect)
            self.screen.blit(den1, den1_rect)
            self.screen.blit(den2, den2_rect)     
        # Multiplying Fraction Problem Type
        if self.question_type == "frac_mult":
            fraction1 = pygame.Rect(fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            fraction2 = pygame.Rect(three_fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            pygame.draw.rect(self.screen, text_color, fraction1)
            pygame.draw.rect(self.screen, text_color, fraction2)
        
            num1 = font.render(self.question[0], True, text_color)
            den1 = font.render(self.question[1], True, text_color)
            num2 = font.render(self.question[2], True, text_color)
            den2 = font.render(self.question[3], True, text_color)
            operator = font.render("x", True, text_color)
            
            num1_rect = num1.get_rect()
            den1_rect = den1.get_rect()
            num2_rect = num2.get_rect()
            den2_rect = den2.get_rect()
            op_rect = operator.get_rect()
            
            num1_rect.center = (third,top)
            den1_rect.center = (third,bot)
            op_rect.center = (half, mid)
            num2_rect.center = (two_third,top)
            den2_rect.center = (two_third,bot)
            
            # blit the question text
            self.screen.blit(num1, num1_rect)
            self.screen.blit(num2, num2_rect)            
            self.screen.blit(operator, op_rect)
            self.screen.blit(den1, den1_rect)
            self.screen.blit(den2, den2_rect)             
        # Dividing Fraction Problem Type   
        if self.question_type == "frac_div":
            fraction1 = pygame.Rect(fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            fraction2 = pygame.Rect(three_fifth, mid, (1/15) * self.WIDTH, (1/120) * self.HEIGHT) 
            pygame.draw.rect(self.screen, text_color, fraction1)
            pygame.draw.rect(self.screen, text_color, fraction2)
        
        
            num1 = font.render(self.question[0], True, text_color)
            den1 = font.render(self.question[1], True, text_color)
            num2 = font.render(self.question[2], True, text_color)
            den2 = font.render(self.question[3], True, text_color)
            operator = font.render("÷", True, text_color)
            
            num1_rect = num1.get_rect()
            den1_rect = den1.get_rect()
            num2_rect = num2.get_rect()
            den2_rect = den2.get_rect()
            op_rect = operator.get_rect()
            
            num1_rect.center = (third,top)
            den1_rect.center = (third,bot)
            op_rect.center = (half, mid)
            num2_rect.center = (two_third,top)
            den2_rect.center = (two_third,bot)
            
            # blit the question text
            self.screen.blit(num1, num1_rect)
            self.screen.blit(num2, num2_rect)            
            self.screen.blit(operator, op_rect)
            self.screen.blit(den1, den1_rect)
            self.screen.blit(den2, den2_rect)           
            
    # Creates the players input (answer) window    
    def init_answer_window(self):
        color1 = self.colors["white"]
        color2 = self.colors["skyblue"]
        color3 = self.colors["paper"]
        text_color = self.colors["black"]
        width = self.WIDTH * .2
        height = self.HEIGHT * .26
        x = self.WIDTH * .11
        y = self.HEIGHT * .4
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color1, rect)
        
        self.negative_ans = False
        # Single answer (integer) input
        if self.two_inputs == False:
            width = self.WIDTH * .125
            height = self.HEIGHT * .14
            x = self.WIDTH * .15
            y = self.HEIGHT * .46
            rect1 = pygame.Rect(x, y, width, height)
            pygame.draw.rect(self.screen, color2, rect1)
           
            self.ans1 = []
            self.ans2 = []
            self.ans_rects = [rect, rect1]
            self.active_ans_window = rect1
        
        # Two answer (fraction) input
        if self.two_inputs == True:
           width = self.WIDTH * .125
           height = self.HEIGHT * .12
           x1 = self.WIDTH * .15
           y1 = self.HEIGHT * .4
           x2 = self.WIDTH * .15
           y2 = self.HEIGHT * .54
           rect1 = pygame.Rect(x1, y1, width, height)
           rect2 = pygame.Rect(x2, y2, width, height)
           pygame.draw.rect(self.screen, color2, rect1)
           pygame.draw.rect(self.screen, color3, rect2)           
           
           fraction = pygame.Rect(.18 * self.WIDTH, .525 * self.HEIGHT, (1/15) * self.WIDTH, (1/120) * self.HEIGHT)
           pygame.draw.rect(self.screen, text_color, fraction)
           
           self.ans1 = []
           self.ans2 = []
           self.ans_rects = [rect, rect1, rect2]
           self.active_ans_window = rect1
    
    # Checks for most current user input and updates the answer input window boxes with input
    def update_answer_window(self):
        # Switches between two answer input boxes if in two input mode
        # Based on mouse click of input window
        if self.game.key_state["left_click"] == True and len(self.ans_rects) > 2:
            (x,y) = pygame.mouse.get_pos()
            if self.active_ans_window == self.ans_rects[1]:
                if pygame.Rect.collidepoint(self.ans_rects[2], (x,y)):
                    font = pygame.font.SysFont("arial", self.HEIGHT // 12, bold=True)
                    color1 = self.colors["skyblue"]
                    color2 = self.colors["paper"]
                    text_color = self.colors["black"]
                    pygame.draw.rect(self.screen, color1, self.ans_rects[2])
                    pygame.draw.rect(self.screen, color2, self.ans_rects[1])
                    self.active_ans_window = self.ans_rects[2]
                    # Draw any existing answer text to opposite input box
                    ans1 = font.render("".join(self.ans1), True, text_color)
                    self.screen.blit(ans1, self.ans_rects[1])
                    # make user numpad input equal to last input of input box
                    self.player_input = self.ans2
            else:
                if pygame.Rect.collidepoint(self.ans_rects[1], (x,y)):
                    font = pygame.font.SysFont("arial", self.HEIGHT // 12, bold=True)
                    color1 = self.colors["skyblue"]
                    color2 = self.colors["paper"]
                    text_color = self.colors["black"]
                    pygame.draw.rect(self.screen, color1, self.ans_rects[1])
                    pygame.draw.rect(self.screen, color2, self.ans_rects[2])
                    self.active_ans_window = self.ans_rects[1]
                    # Draw any exisiting answer text toopposite input box
                    ans2 = font.render("".join(self.ans2), True, text_color)
                    self.screen.blit(ans2, self.ans_rects[2])
                    # make user numpad input equal to last input of input box
                    self.player_input = self.ans1

        # Init Font Variables
        font = pygame.font.SysFont("arial", self.HEIGHT // 12, bold=True)
        color = self.colors["skyblue"]
        text_color = self.colors["black"]
        # Input boxes are not currently being switched -- update current input boxes w/ user numpad input
        # If two inputs (fraction answer)
        if len(self.ans_rects) > 2:
            # Clear and then update top answer box
            if self.active_ans_window == self.ans_rects[1]:
                pygame.draw.rect(self.screen, color, self.ans_rects[1])
                self.ans1 = self.player_input
                ans1 = font.render("".join(self.ans1), True, text_color)
                self.screen.blit(ans1, self.ans_rects[1])
            # Clear and then update bottom answer box
            else:
                pygame.draw.rect(self.screen, color, self.ans_rects[2])
                self.ans2 = self.player_input
                ans2 = font.render("".join(self.ans2), True, text_color)
                self.screen.blit(ans2, self.ans_rects[2])
        # Clear and then update single answer box
        else:
            pygame.draw.rect(self.screen, color, self.ans_rects[1])
            self.ans1 = self.player_input
            ans1 = font.render("".join(self.ans1), True, text_color)
            self.screen.blit(ans1, self.ans_rects[1])
                 
    # Makes a grid of buttons used as players input number pad
    def init_numpad(self):
        # def numpad button variables
        button_width = int((1.5/30) * self.WIDTH)
        button_height = int((1.5/30) * self.HEIGHT)
        rows = 5    # num of button rows
        columns = 3 # num of button columns
        color = self.colors["skyblue"]
        start_x = self.WIDTH * .005 # starting x coord of numpad button menu
        start_y = self.HEIGHT * .76 # starting y coord of numpad button menu
        # def numpad button text list
        button_text = ["7", "4", "1", "8", "5", "2", "9", "6", "3", "←", "+ / -", "0", "CLEAR", "ENTER", "_ ↔ ½"]
        text_index = 0
        font = pygame.font.SysFont("arial", 22, bold=True)
        text_color = self.colors["black"]
        text_rects = []
        self.numpad_input = {}
        for x in range(1, rows+1, 1):
            for y in range(1, columns+1, 1):
                rect = pygame.Rect(start_x + x * button_width * 1.1, start_y + y * button_height * 1.1, button_width, button_height) # Create a button
                self.numpad_input[button_text[text_index]] = rect   # store each button rect in dictionary use btn text as key
                text = font.render(button_text[text_index], True, text_color)
                text_rect = text.get_rect()
                text_rect.topleft = (rect.x + (rect[2] - text_rect[2]) // 2, rect.y + (rect[3] - text_rect[3]) // 2) # Overlays each text rect x,y coords to match center of each buttons
                pygame.draw.rect(self.screen, color, rect) # Draw each button to screen 
                self.screen.blit(text, text_rect) # Blit button text
                text_index += 1 # Increment the button_text list index
                
        # Init player input variable
        self.player_input = []
        self.left_down = False
        
    def init_scratchpad(self):
        scratchpad_image = pygame.image.load("math_game/images/paper.png") #Scratchpad image
        scratchpad_image = pygame.transform.scale(scratchpad_image, (int(.55 * self.WIDTH),int(.78 * self.HEIGHT))) # Scale to screen
        scratchpad_rect = scratchpad_image.get_rect()
        # Scratchpad rect (X, Y, WIDTH, HEIGHT), creates drawing "boundaries"
        self.scratchpad_rect = pygame.Rect(self.WIDTH//2.25 + .11 * scratchpad_rect[2], .0575 * scratchpad_rect[3], .8 * scratchpad_rect[2], .8 * scratchpad_rect[3])
        self.scratchpad_obj = (scratchpad_image, (self.WIDTH//2.25, 0))
        
        self.draw_objects.append(self.scratchpad_obj)        
        
    # Creates a button menu for the player's scratchpad    
    def init_scratchpad_menu(self):
        # Load menu button image and create image rect
        menu_image = pygame.image.load("math_game/images/draw_menu.png")
        menu_image = pygame.transform.scale(menu_image, (int(.25*self.WIDTH),int(.175*self.HEIGHT))) # Scale to screen
        menu_obj = (menu_image, (self.WIDTH * .75, self.HEIGHT * .8))
        menu_rect = menu_image.get_rect()
        menu_rect = pygame.Rect.move(menu_rect, self.WIDTH * .75, self.HEIGHT *.8)
        
        self.draw_objects.append(menu_obj)
        
        # Assign menu image rect dimensions and coordinates to temp vars
        x = menu_rect[0]
        y = menu_rect[1]
        w = menu_rect[2]
        h = menu_rect[3]
        
        # Init scratchpad menu button coordinates and dimensions
        # (Creates/overlays the menu "button" locations and sizes on the menu image)
        self.scratchpad_menu = { 
                                "black" : pygame.Rect(x + x*.017, y + y*.017, w * .085, h * .14),
                                "yellow":  pygame.Rect(x + x*.039, y + y*.017, w * .085, h * .14),
                                 "red":  pygame.Rect(x + x*.071, y + y*.017, w * .085, h * .14),
                                 "orange":  pygame.Rect(x + x*.101, y + y*.017, w * .085, h * .14),
                                 "blue":  pygame.Rect(x + x*.133, y + y*.017, w * .085, h * .14),
                                 "green":  pygame.Rect(x + x*.165, y + y*.017, w * .085, h * .14),
                                 "pencil":  pygame.Rect(x + x*.016, y + y*.07, w * .24, h * .4),
                                 "eraser":  pygame.Rect(x + x*.116, y + y*.07, w * .24, h * .4),
                                 "thickness":  pygame.Rect(x + x*.226, y + y*.07, w * .25, h * .4),
                                 "clear":  pygame.Rect(x + x*.22, y + y*.015, w * .26, h * .18)  }
                                                           
        # Default scratchpad variables (line color and thickness)
        self.line_color = self.colors["black"]
        self.line_thickness = 2
        
    # Checks for scratchpad menu changes / button selections.
    def scratchpad_menu_check(self):
        if self.game.key_state["left_click"] == True:
            (x,y) = pygame.mouse.get_pos()
            
            pressed_button = None
            for button, rect in self.scratchpad_menu.items():
                if pygame.Rect.collidepoint(rect, (x,y)):
                    pressed_button = button
                    
            # Pencil color selection
            for color in self.colors:
                if pressed_button == color:
                    self.line_color = color
                    self.line_thickness = 1.5
            if pressed_button == "eraser":
                self.line_thickness = 18
                self.line_color = self.colors["paper"]
            if pressed_button == "pencil":
                self.line_thickness = 2
                self.line_color = "black"
            if pressed_button == "thickness":
                    if self.line_thickness < 6:
                        self.line_thickness = self.line_thickness + .1
            # Clear scratchpad by redrawing a new image
            if pressed_button == "clear":
                self.draw_objects.append(self.scratchpad_obj)
    
    # Updates the scratchpad with the player's current drawing
    def update_scratchpad(self):            
        if self.game.key_state["left_click"] == True and self.left_click == False:
            (self.x1,self.y1) = pygame.mouse.get_pos()
            self.left_click = True
        if self.left_click == True:
            (self.x2,self.y2) = pygame.mouse.get_pos()
            
            # If players mouse is within the scratchpad, then draw, else don't draw
            if pygame.Rect.collidepoint(self.scratchpad_rect, (self.x1,self.y1)):
                # Ensures lines are drawn consecutively instead of fragmented --
                # steps = the greater value of the pen's moved distance in either the x or y direction since last iteration
                steps = max(abs(self.x2 - self.x1), abs(self.y2 - self.y1))   
                if steps != 0:
                    # Calc ratios of x to y movement since last iteration over the distance moved (change in x vs. change in y)
                    dx = (self.x2 - self.x1) / steps                             
                    dy = (self.y2 - self.y1) / steps
                    # Draw a "dot" for every x,y position, ensuring a smooth, continuous, line is drawn
                    for each in range(steps):
                        self.x1 += dx
                        self.y1 += dy
                        if pygame.Rect.collidepoint(self.scratchpad_rect, (self.x1, self.y1)):
                            pygame.draw.circle(self.game.screen, self.line_color, (self.x1,self.y1), self.line_thickness)
            # Update the next iterations initial coordinates   
            (self.x1,self.y1) = (self.x2,self.y2)
        
        if not self.game.key_state["left_click"]:
            self.left_click = False
    
    # Checks for player numpad inputs during game
    def numpad_check(self):
        if self.game.key_state["left_click"] == True:
            self.left_down = True
        # Executes when left click is released
        if self.game.key_state["left_click"] == False and self.left_down == True:
            self.left_down = False
            (x,y) = pygame.mouse.get_pos()
            pressed_button = None
            for button, rect in self.numpad_input.items():
                if pygame.Rect.collidepoint(rect, (x,y)):
                    pressed_button = button
            try:
                pressed_button = int(pressed_button)
            except:
                pass
            # If number button pressed, add to player input
            # Do not let player input length exceed 4 digits
            # (Overwrite the last digit)
            if type(pressed_button) == int:
                if len(self.player_input) > 3:
                    self.player_input.pop()
                self.player_input.append(str(pressed_button))
            # Backspace
            if pressed_button == "←":
                if self.player_input:
                    self.player_input.pop()
            # Toggle negative sign
            if pressed_button == "+ / -":
                self.toggle_negative_ans()
            # Clear input list
            if pressed_button == "CLEAR":
                self.player_input = []
                self.init_answer_window()
            if pressed_button == "ENTER":
                self.submit_answer()
            if pressed_button == "_ ↔ ½":
                self.player_input = []
                self.toggle_input_screen()
    
    # Switches between 1 or 2 answer input windows
    def toggle_input_screen(self):
        if self.two_inputs == False:
            self.two_inputs = True
        else:
            self.two_inputs = False
        
        self.init_answer_window()
    
    # Toggles between a positive or negative answer (and displays it)
    def toggle_negative_ans(self):
        color = self.colors["white"]
        text_color = self.colors["black"]
        x = self.ans_rects[0].x
        y = self.ans_rects[0].y + (1/4) * self.ans_rects[0].h
        coords = (x,y)
        font = pygame.font.SysFont("arial", self.HEIGHT // 12, bold=True)
        neg = font.render("-", True, text_color)
        neg_rect = neg.get_rect()
        w = neg_rect.w
        h = neg_rect.h
        if self.negative_ans == False:
            self.negative_ans = True
            font = pygame.font.SysFont("arial", self.HEIGHT // 12, bold=True)
            neg = font.render("-", True, text_color)
            self.screen.blit(neg, coords)   
        else:
            self.negative_ans = False
            rect = pygame.Rect(x, y, w, h)
            pygame.draw.rect(self.screen, color, rect)
    
    # Submits answer to current question
    def submit_answer(self):
        # If ans1 box is empty, don't submit answer
        if not self.ans1:
            return
        # Make ans1 a negative, if selected
        if self.negative_ans == True:
            self.ans1[0] = str(int(self.ans1[0]) * -1)
        # Join togeather input lists
        self.ans1 = "".join(self.ans1)
        self.ans2 = "".join(self.ans2)

        # Question requires two input answer (fraction)
        if len(self.correct_answer) > 1:
            # Correct answer -- add points to score and increment multiplier
            if self.ans1 == self.correct_answer[0] and self.ans2 == self.correct_answer[1]:
                self.player_score = self.player_score + self.CORRECT_ANS_POINTS * self.score_mult_count
                # Ensure score multiplier does not exceed max value, otherwise, increment
                if self.score_mult_count < self.SCORE_MULT_MAX:
                    self.score_mult_count += 1
            # Incorrect answer -- reset multiplier
            else:
                self.score_mult_count = 1
        # Question requires single input answer (integer)
        else:
            # Correct answer -- add points to score and increment multiplier
            if self.ans1 == self.correct_answer[0] and not self.ans2:
                self.player_score = self.player_score + self.CORRECT_ANS_POINTS * self.score_mult_count
                # Ensure score multiplier does not exceed max value, otherwise, increment
                if self.score_mult_count < self.SCORE_MULT_MAX:
                    self.score_mult_count += 1
            # Incorrect answer -- reset multiplier         
            else:
                self.score_mult_count = 1
        
        #print(self.ans1, self.ans2, "Score:", self.player_score, "Multiplier: ", self.score_mult_count)
        
        # Update score changes to screen
        self.update_game_score()
        # Reset all inputs
        self.player_input = []
        self.init_answer_window()
        # Next Question -- generates new question window which calls generate_question()
        self.init_question_window()

    def update_game_score(self):
     # Create multiplier window
        width = self.WIDTH * .3
        height = self.HEIGHT * .6
        x = self.WIDTH * .4
        y = self.HEIGHT * .86
        color = self.colors["yellow"]
        text_color = self.colors["blue"]
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)
        font = pygame.font.SysFont("arial", self.HEIGHT // 17, bold=True)
        score = font.render("Multiplier: " + str(self.score_mult_count) + "x", True, text_color)
        self.screen.blit(score, rect)
   
        # Create score window
        y = self.HEIGHT * .92
        text_color = self.colors["red"]
        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, color, rect)
        font = pygame.font.SysFont("arial", self.HEIGHT // 17, bold=True)
        score = font.render("Score: " + str(self.player_score), True, text_color)
        self.screen.blit(score, rect)
        
    
    # Draws all images to screen    
    def draw(self, objects):
        for each in objects:
            self.screen.blit(each[0],each[1])
        self.update_scratchpad()
        pygame.display.update()
    
    # Main Math game loop
    def game_loop(self):
        while self.game.running and self.math_running:
        
            self.game.get_events()
            self.scratchpad_menu_check()
            self.numpad_check()
            self.update_answer_window()
            self.update_game_timer()
            
            self.draw(self.draw_objects)
            self.draw_objects = [] # Empty list after draw
            
            self.game.clock.tick(self.FPS)
    
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
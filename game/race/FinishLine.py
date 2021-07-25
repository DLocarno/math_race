import pygame

# Finish line class creates a "finish line" object and keeps track
# of the laps of the race, as to know when a "win/lose" condtion is met.
class FinishLine:

    def __init__(self, level, game_objects, game):
        # Extract coordinates
        self.coords = level.finish_line_coords
        # Extract No. of laps for Level
        self.laps = level.laps
        # Create reference to all game objects
        self.game_objects = game_objects
        # Running variables
        self.game = game

        # Init vars to create finish line surface
        x = self.coords[0]
        y = self.coords[1]
        w = self.coords [2]
        h = self.coords[3]
        angle = self.coords[4]
        color = self.coords[5]
        
        # Create the finish line surface
        fl = pygame.Surface((w,h))
        # Color
        fl.fill(color)        
        
        # Finish line text
        fl_font = pygame.font.SysFont("comicsansms", int(.05 * y), bold=True)
        fl_text = fl_font.render("F I N I S H", True, (0,0,0)) # Black Color Text
        # Center Finish Line Text to Finish Line Surface
        fl_text_rect = fl_text.get_rect()
        text_x = (w - fl_text_rect.w) // 2
        text_y = (h - fl_text_rect.h) // 2
        # Append finish line text to finish line surface
        fl.blit(fl_text, (text_x, text_y))
        
        # Init vars to be used by PlayerView Class to draw the finish line
        self.finish_line = fl
        self.coords = (x,y)
        
        # Split the bottom half and top half of Finish Line Surface
        # and create seperate rects for collisioning and lap incremeneting
        self.top = pygame.Rect(x, y, w, h * .5)
        self.bottom = pygame.Rect(x, y + h * .5, w, h * .5)
        # Init empty lists to track car rects and collision booleans
        self.cars = []          # Car objects
        self.car_rects = []     # Car object rectangles
        self.collisions = []    # Collision boolean list for every car object        
        # Init race results list
        self.race_results = []

     # Detects collisions with in-game objects and increments lap count for players   
    def update(self):
        # Update car rects list on every iteration, to get new coords of every car rect
        if self.collisions:
            self.car_rects.append(self.game_objects["player_car"].rect)
            for car in self.game_objects["npc_cars"]:
                self.car_rects.append(car.rect)
        # If this is the first call to update, init collisions and car object lists
        else:
            self.car_rects.append(self.game_objects["player_car"].rect)
            self.collisions.append([False, False])
            self.cars.append(self.game_objects["player_car"])
            for car in self.game_objects["npc_cars"]:
                self.car_rects.append(car.rect)
                self.collisions.append([False, False])
                self.cars.append(car)

        # For every car, detects collision with both (top and bottom) sides of the finish line
        # The "bottom" and "top" collision list variables will then get the list index of the
        # car rect element stored in the self.cars list corresponding to the in-game car colliding
        bottom_collisions = pygame.Rect.collidelistall(self.bottom, self.car_rects)
        top_collisions = pygame.Rect.collidelistall(self.top, self.car_rects)
        
        # For each collision detected with the lower half of the finish line
        for i in bottom_collisions:
            # If Car is ONLY in bottom half of finish line
            if i not in top_collisions:
                self.collisions[i][0] = True # set bottom collision to True
                self.collisions[i][1] = False # set top collision to False
            # Player has continued to move backwards over finish line, decrement car's lap count
            elif self.collisions[i][1] == True:
                self.cars[i].lap_count -= 1
                self.collisions[i][1] = False
        
        # For each collision detected with the upper half of the finish line
        for i in top_collisions:
            if i not in bottom_collisions:
                self.collisions[i][1] = True # Set Top to True
            # Player has continued over the finish line, increment car's lap count   
            elif self.collisions[i][0] == True:
                self.cars[i].lap_count += 1
                self.collisions[i][0] = False
              

                ################### WIN CONDITION ####################################
                ## TO DO: (MAKE THIS BETTER)
                # If car reaches race's lap count, update race results list
                if self.cars[i].lap_count > self.laps and i not in self.race_results:
                    self.race_results.append(i)
                    # Player finished, display results, end race
                    if i == 0 and len(self.race_results) == 1:
                        print("Congrats, you Won.")
                        self.game.running = False
                    elif i == 0:
                        print("Congrats, you came in:", len(self.race_results))
                        print("Race Results: ")
                        for i in range(0, len(self.race_results), 1):
                            print("Player:", self.race_results[i] + 1, "came in ", i + 1)
                        self.game.running = False
                ########################################################################
        
        # Empty car rect list for next iteration
        self.car_rects = []

        
        
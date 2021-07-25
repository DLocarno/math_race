import pygame
import os
# Defines parent class to any in-game objects with an image
class ImageObject:

    def __init__(self, coords, image_file = None):
        self.x = coords[0]
        self.y = coords[1]
        if len(coords) > 2:         # If this object has a start angle in its 'coords' argument
            self.angle = coords[2]  # Init the start angle
            self.image_basename = os.path.splitext(image_file)[0]         # Truncates the file name to get a basename for the image file (used in car objects' rotation methods)
            self.image_file = self.image_basename + "_" + str(self.angle) + ".png" # Append the start angle to image_file name
        else:
            self.image_file = image_file # Image object had no start angle (such as a level map)
        
        self.image = pygame.image.load(self.image_file)  # Load the image file
        self.image.set_colorkey("white")
        self.image.convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        self.collision_level = False
        self.collision_player = False
        self.collision_right = False
        self.collision_left = False
        self.collision_up = False
        self.collision_down = False
        self.collision_counter = 0
        self.collision_count = None # During obj collisions, this is set to either of the two constants below
        self.collision_constant_level = (50, 5)  # Constants used for smooth collisioning movement with level (50, 5) seem to work well
        self.collision_constant_player = (80, 20) # Same as above, but, for collisions between players 

class SimpleObject:

    def __init__(self, coords, dims):
        self.coords = coords
        self.dims = dims

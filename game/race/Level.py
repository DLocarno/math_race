import pygame
import os

from race.GameObject import ImageObject
 
 
class Level(ImageObject):
    
    def __init__(self, image_file):
        super().__init__((0,0), image_file)
        
        self.path = os.path.split(image_file)
        self.parent_directory = self.path[0]                # parses parent folder name of image
        self.level_name = os.path.splitext(self.path[1])[0] # parses level from filename
        
        # Variables needed to store level init data which will be read from the level init datafile
        self.level_boundary_color = None
        self.finish_line_coords = None
        self.player_start_coords = None
        self.npcs = None
        self.npc_start_coords = []
        self.npc_points = []
        
        # Read the data from the level's .txt data file
        self.get_level_init_data()
    
    # Gets corresponding level data to the level image file passed as the objects argument
    def get_level_init_data(self):
        try:
            with open(self.parent_directory + "/" + self.level_name + "_init_data.txt") as file:
                text_data = file.readlines()
        except:
            print("Required level datafile doesn't exist")
            return None
        
        # Parse the list and extract only the relevent data
        text_data = [line for line in text_data if not line.startswith("#")] # remove all lines starting with # symbol
        text_data = [el.strip() for el in text_data]                         # remove all newline chars
        text_data = [el for el in text_data if el != ""]                     # remove all blank string entries (empty lines)                        
        
        # Use .eval() method to convert each element in list into the right datatype (integer, tuple, etc.)
        data = []
        for each in text_data:
            each = eval(each)
            data.append(each)
        
        # Get number of Laps for Race
        self.laps = data[0]
        # Get Level Boundary Color
        self.level_boundary_color = data[1]
        # Get Finish Line Coords
        self.finish_line_coords = data[2]
        # Get player start coordinate data (x,y,angle (deg))
        self.player_start_coords = data[3]
        # Get num of non-playable characters and their start coords (x,y,angle (deg))
        self.npcs = int(data[4])
        for i in range(5, self.npcs + 5, 1):    # Shift index of loop to start at waypoint data
            self.npc_start_coords.append(data[i])
        # Get npc waypoint coordinates for level (ie. points NPC's will control to)
        n = i + 1
        for i in range(n, len(data), 1):
            self.npc_points.append(data[i])
            
        # Pygame functions to convert the level image and create a mask of image used for collision detect with the level--
        # Set level background color & onvert alpha
        self.image.set_colorkey("white")
        self.image.convert_alpha()
        # Set mask color used for level boundary (level collision color read from data file)
        #Note: Second argument is a color sensitivity threshold--could need adjusment
        self.mask = pygame.mask.from_threshold(self.image, pygame.Color(self.level_boundary_color), (1,1,1,1))
        
        print("\nExtracted all level data from file.")
        print("No. Laps:", self.laps)
        print("Level Boundary Color:", self.level_boundary_color)
        print("Finish line data:", self.finish_line_coords)
        print("Player start coords:", self.player_start_coords)
        print("Number of NPCs:", self.npcs)
        print("NPC start coords:", self.npc_start_coords)
        print("")
        
    def update(self):
        self.rect = self.image.get_rect()
        
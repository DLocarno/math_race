import pygame

from race import GameObject

# Player class creates a 'viewport' (camera) for the player.  Recieves map and game object data
# and draws everything to the viewport surface, before the final output is drawn to screen. 
class PlayerView:
    # Initializes the player's viewport
    def __init__(self, screen, game_objects):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.screen_width = self.screen_rect[2]
        self.screen_height = self.screen_rect[3]
        self.game_objects = game_objects
        self.level = game_objects["level"]
        self.finish_line = game_objects["finish_line"]
        self.player = game_objects["player_car"]
        self.player_rect = self.player.rect
        self.npc_cars = game_objects["npc_cars"]
        
        self.level_image = self.level.image # racetrack image
        self.player_image = self.player.image
        # Create the viewport    
        self.viewport = pygame.Surface((self.screen_width, self.screen_height))
 
    # Updates any needed in-game object info and viewport coords
    def update_viewport(self):
        # Offset calculation -- calculates center of where the viewport (player's view) needs to be,
        # based on initial screen size and the player's sprite image size
        self.player_offset_x = (self.screen_width / 2) - (self.player.rect[2] / 2)
        self.player_offset_y = (self.screen_height / 2) - (self.player.rect[3] / 2)
        
        self.viewport.fill((255,255,255)) # Fill background of viewport white
        # Updates viewport coords 
        #(-1 moves viewport in equal and opposite movement of player)
        self.x = -1 * self.player.rect.x
        self.y = -1 * self.player.rect.y
        # Account for the offset
        self.x = self.x + self.player_offset_x
        self.y = self.y + self.player_offset_y
        
    # Draws map & all in-game objects to viewport, then draws viewport to screen
    def display_viewport(self):

        self.viewport.blit(self.level_image, (self.x, self.y))                              # draw the level image to viewport
        self.level_image.blit(self.finish_line.finish_line, self.finish_line.coords)        # draw the finsih line to the level image
        self.viewport.blit(self.player.image, (self.player_offset_x, self.player_offset_y)) # draw car to center of viewport
        
        for self.npc in self.npc_cars:
            self.viewport.blit(self.npc.image, (self.x + self.npc.x, self.y + self.npc.y))         # draw all NPC's
        
        self.screen.blit(self.viewport, (0, 0)) # draw viewport to screen
        


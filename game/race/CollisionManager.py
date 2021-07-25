import pygame

# This class inits a manager object for every instantiated player object (human and NPC), which 
# they use to detect their in-game collisions between the level's boundaries and other player objects
class CollisionManager:

    def __init__(self, parent_object, game_objects):
        self.parent_object = parent_object                            # Set the collision managers owner object
        self.level = game_objects["level"]                            # Get the level object
        self.collision_object_list = []                               # Create a collision list for all game objects
        
        # Add all other in-game objects to a collsion object list (except the manager's parent object)
        if game_objects["player_car"] != self.parent_object:
            self.collision_object_list.append(game_objects["player_car"])
        for npc in game_objects["npc_cars"]:
            if npc != self.parent_object:
                self.collision_object_list.append(npc)
        
        # required vars
        self.offset = None
        self.overlap = None
        self.obj_collision = None
    
    # Each in-game object will make a call to its manager once per every race loop iteration.
    # in order to detect/calculate any collisions with any other in-game objects
    def get_collisions(self):   
        # Test objects against other in-game objects
        for player in self.collision_object_list:
            self.determine_player_collisions(self.parent_object, player)
        # NOTE: the following break statement is important to understand--
        # Once a collision with another object is detected, we must break this loop, 
        # so that the next comparison with the next game object won't overwrite the collision
        # variables.  In otherwords, collision detection with other objects is greedy.
            if self.parent_object.collision_player == True:
                break
        # Test object for collisions against the level - Always test level after player, to
        # Ensure all players stay in-bounds.
        self.determine_level_collisions(self.parent_object, self.level)

        
    # Calculates if a collision exists between in-game objects and the level map
    def level_calc_offset(self, obj, x = None, y = None):
        if x == None and y == None: # First iteration call
            self.offset = (obj.rect.x - self.level.rect.x, obj.rect.y - self.level.rect.y)
            self.overlap = self.level.mask.overlap(obj.mask, (self.offset))
        else: # Any subsequent calls during the same iteration 
            self.offset = (x - self.level.rect.x, y - self.level.rect.y)
            self.overlap = self.level.mask.overlap(obj.mask, (self.offset))   
    
    # Used to determine where (which side) of the sprite image is colliding with the level
    # by moving the sprite's rectangle slightly and re-checking for the collision.
    # Then, if the collision still exists, we know the collision was in that direction
    def determine_level_collisions(self, obj, level):
        # Temporary rect coordinates used in re-calcs 
        x = obj.rect.x
        y = obj.rect.y
        # 50 px rect offsets used in the calc 
        #(This would be dependent on image size of the car/player, fortunately, they're all the same size).
        X = 50                 
        Y = 50
        
        # Check to see if a collision exists
        self.level_calc_offset(obj)
        # A collision was detected, now we need to find where on the sprite image.
        if self.overlap:
            # Calcs to find where the collision is. And, sets player's variables accordingly
            obj.collision_level = True
            x += X
            self.level_calc_offset(obj, x, y) # Subsequent calls used to determine which side collision occured
            if self.overlap:
                obj.collision_right = True
                obj.collision_left = False
            x = obj.rect.x
            y = obj.rect.y
            x -= X
            self.level_calc_offset(obj, x, y)
            if self.overlap:
                obj.collision_left = True
                obj.collision_right = False
            x = obj.rect.x
            y = obj.rect.y
            y += Y
            self.level_calc_offset(obj, x, y)
            if self.overlap:
                obj.collision_down = True
                obj.collision_up = False
            x = obj.rect.x
            y = obj.rect.y
            y -= Y
            self.level_calc_offset(obj, x, y)
            if self.overlap:
                obj.collision_up = True
                obj.collision_down = False

        # No collision with the level is detected, ensure variable is reset
        else:
            obj.collision_level = False

    # Same as level_calc_offset, except used between 2 players
    # For this method, we don't care about the image mask, because we aren't worried about
    # a collsiion with a specific color, only that the rect's of the game images overlap/collide.
    def player_detect_collision(self, rect1, rect2):
        self.obj_collision = pygame.Rect.colliderect(rect1, rect2) # returns -1 if no collision

    def determine_player_collisions(self, obj1, obj2):
        #  x,y temp coords for just one object
        # (If we determine which "side" the collision has occured for one object,
        # then we know it must be the opposite "side" on the other object)
        rect1 = obj1.rect
        rect2 = obj2.rect

        # Rect offset constants again (again may need to be changed depending on sprite image size)
        X = 50
        Y = 50
        # Calc the offset of the image masks
        self.player_detect_collision(rect1, rect2)
        
        # If a collision between players was detected, perfoms calcs
        # moving the rects coords of each obj and makes subsequent calls
        # player_detect_collisions, to find where/which side the collision is on. 
        # And, then sets each player object's variables accordingly
        if  self.obj_collision:
            obj1.collision_player = True    # Set obj1 into a collision state
            obj2.collision_player = True    # Set obj2 into a collision state
            
            # Move copy of obj2 rect's coords in different directions and re-test
            # Until every side of object rects are tested and determined
            temp_rect = obj2.rect.copy()
            temp_rect.x += X
            self.player_detect_collision(rect1, temp_rect)
            if self.obj_collision:
                obj2.collision_right = True
                obj2.collision_left = False
                obj1.collision_right = False
                obj1.collision_left = True
            temp_rect = obj2.rect.copy()
            temp_rect.x -= X
            self.player_detect_collision(rect1, temp_rect)
            if self.obj_collision:
                obj2.collision_left = True
                obj2.collision_right = False
                obj1.collision_left = False
                obj1.collision_right = True
            temp_rect = obj2.rect.copy()
            temp_rect.y += Y
            self.player_detect_collision(rect1, temp_rect) 
            if self.obj_collision:
                obj2.collision_down = True
                obj2.collision_up = False
                obj1.collision_down = False
                obj1.collision_up = True
            temp_rect = obj2.rect.copy()
            temp_rect.y -= Y
            self.player_detect_collision(rect1, temp_rect) 
            if self.obj_collision:
                obj2.collision_up = True
                obj2.collision_down = False
                obj1.collision_up = False
                obj1.collision_down = True
                

        #No collision between the two objects are detected, ensure variables are reset
        else:
            obj1.collision_player = False
            obj2.collision_player = False
           # if self.parent_object == self.game_objects["player_car"]:
             #   print("No collision.", obj1.collision_player)
             #   print("R:", obj1.collision_right, "L:", obj1.collision_left, "U:", obj1.collision_up, "D", obj1.collision_down)

        
        
        
        
        

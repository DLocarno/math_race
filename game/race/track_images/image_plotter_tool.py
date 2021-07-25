from PIL import Image, ImageTk
import tkinter as tk
import os
import sys
import time

# This script creates a plot map (datafile) consisting of rendezvous points (x & y pixel locations)
# by clicking on a game level map (track) for the NPC players to travel along
# Requires use of Tkinter as the GUI interface and PIL at the image handling tool.
# Accepts the image as the scripts paremeter. Outputs a text file.
Image.MAX_IMAGE_PIXELS = 280000000

class ImagePlotterTool:
    
    def __init__(self, root, file_name):
        self.root = root
        self.base_name = os.path.splitext(file_name)[0] # Get the files base name
        self.output_filename = self.base_name + "_npc_waypoints" + ".txt"
        self.image = Image.open(file_name)
        self.image_copy = self.image.copy()
        self.window_w = 1400
        self.window_h = 900
        self.plot_series = []       # list to keep track of a series of plot points
        self.plot_points = []       # list to keep track of all plot point series
        # Method calls
        self.set_root_geometry()
        self.get_image_data()
        self.resize_image()
        self.image_canvas()
        self.create_key_events()

    
    # Sets screens window gemoetry
    def set_root_geometry(self):
        self.root.geometry(str(self.window_w)+"x"+str(self.window_h))
    
    # Gets actual pixel w x h of image, then performs the conversion ratio needed & assigns to vars
    def get_image_data(self):
        image_w, image_h = self.image.size
        self.conversion_ratio_x = image_w / self.window_w
        self.conversion_ratio_y = image_h / self.window_h
    
    # Resizes a copy of the image (which may be very large) to be displayed on the screen canvas 
    def resize_image(self):
        self.image_copy = self.image_copy.resize((self.window_w, self.window_h))
          
    # Constructs a canvas window, converts the image, and overlays the image copy to the canvas and displays it
    def image_canvas(self):
        self.canvas = tk.Canvas(root, width=self.window_w, height=self.window_h)    
        self.canvas.pack()                                                                                      
        self.image_tk = ImageTk.PhotoImage(self.image_copy)                                                   
        self.canvas.create_image(self.image_copy.size[0]//2, self.image_copy.size[1]//2, image=self.image_tk) 
    
    # Bind key input events to Tkinter GUI interface.
    # Left click adds a plot point (x,y pixel coordinates from image) to a 'series' of plot points
    # Right click will append all of the last series of added points to a new line in the datafile to be outputted
    def create_key_events(self):
        self.root.bind("<Escape>", self.terminate) # Esc key terminates
        self.canvas.bind("<Button-1>", self.add_point) #left mouse click
        self.canvas.bind("<Button-2>", self.plot_points_to_line) # right mouse click
        self.canvas.bind("<Button-3>", self.plot_points_to_line) # Also, can be right mouse click (hardware dependent)
        self.root.bind("<BackSpace>", self.undo_last_point) # Removes the last point added to the current series
        self.root.bind("<Return>", self.output_to_file) # Enter button outputs all plot points
        
    # Adds a the x and y image coordinates to a list
    def add_point(self, event):
        point_x = int(event.x * self.conversion_ratio_x)
        point_y = int(event.y * self.conversion_ratio_y)
        coords = (point_x, point_y)
        self.plot_series.append(coords)
        print("Point at: ", point_x, point_y, "added.")
    
    def undo_last_point(self, event):
        if self.plot_series:
            point = self.plot_series.pop()  # Remove the last point added
            print("Point at: ", point, "removed.")
        else:
            print("No points to remove")
        
    def plot_points_to_line(self, event):
        
        if self.plot_series:
            self.plot_points.append(self.plot_series)
            print("Point series added.")
            self.plot_series = []    # Start new series
        else:
            print("No plots to add.")
            
    # Outputs all point series to .txt file, one point series per line.
    def output_to_file(self, event):
        print("Writing plot points:", self.plot_points, "to file.")
        
        # Make sure there's plots to write to
        if not self.plot_points:
            print("There are no plot points to write")
            return None
        
        # If file doesn't exist, create the file
        if not os.path.exists(self.output_filename):
            file = open(self.output_filename, "a")
        else:
            print("A file with that output name already exists. Delete the file first.")
            return None
            
        # Write to it, one series per line
        for plot_series in self.plot_points:
            file.write(str(plot_series))
            file.write("\n")
        file.close()
        self.plot_series = []
        self.plot_points = []
        
        print("Finished.")
    
    def terminate(self, event):
        self.root.destroy()
    
     

# Main
# accepts the full image filename as the scripts command line argument

image_filename = sys.argv[1]
root = tk.Tk()
win = ImagePlotterTool(root, image_filename)
root.mainloop()
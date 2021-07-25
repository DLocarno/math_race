Original work Copyright (c) 2021 David Locarno

-----------------------------------------------------------------------

Game Requirements:
Windows OS (Tested on Windows 10 only)
Python3 (Original code written with Python ver 3.9.4)
Python Package Installer (PIP) - Used to install python modules
Note: To install PIP on windows:
Open cmd prompt and enter:
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
python get-pip.py
To verify installation:
pip help
To update pip to the newest version, enter:
python -m pip install --upgrade pip

-------------------------------------------------------------------

Required Python Modules:
pygame (ver 2.0.1 used)
random
os
sys
time
math
fractions

To install modules, use PIP
Example of using pip to install pygame--
open Windows cmd prompt, enter:
pip install pygame

To see a list of all modules previously installed with PIP, enter:
pip list

To see a list of all Python modules installed, open command prompt, type: idle
In idle shell, type: help("modules")

---------------------------------------------------------------------------------------------------------
Optional Modules (required to use game dev tools):
pillow
tkinter (ver 8.6)
----------------------------------------------------------------------------------------------------------
TO RUN THE GAME:
1) Download all source code files, data files, and game images and keep default file heiarchy. 
2) Ensure above requirements are met (python installed with all required modules) and PATH environment var is set.
3) Stage uncompressed source code in an accessible directory. Ensure all executable file permissions.
4) Open windows command prompt
5) cd [gamedirectory path]
6) In prompt, type:
	python main.py

------------------------------------------------------------------------------------------------------------

IMPORTANT NOTES:
1) The main directory "game" folder defines the main.py class, which inits the game and is used to handle transitions between game sequences and pass critical data between them.
2) In the main directory, the ImproveAttributes.py class file contains modifiable variables to adjust the base attribute values of human-playable character.
3) Game uses .txt transcript files, containing its in-game character' text.  These can be editable, as desired, but must end with *END, which is used as the parser code's delimeter.
4) The "race" subdirectory contains all the source code pertaining to the "car-race" portion of the game.  May view/edit race.py file to modify critical race data including NPC attributes.
5) Each level image file is stored in the "race/track_images" subdirectory.  Accompanying each level .PNG image file, is a critical text file, such as "track_1_init_data.txt".
   This contains critical initialization data for the corresponding level (the filenaming convention is critical) and without it, the level cannot initialize.
   These files are editable, but, must follow a strict format.  For more information, navigate to one of these files and view in a text editor.
6) The "math_game" subdirectory contains all of the source code pertaining to the "math problem" portion of the game.  Contains editable variables which influence the game's timer and scoring system. 


GAME FEATURES / TOOLS:
The /game/race/track_images directory contains a script: "image_plotter_tool.py" file which accepts a new level image (.PNG) file as an argument.  Can be used to quickly plot and output NPC waypoints for a new level.
To use this tool, run script in cmd prompt and pass any level image (.PNG) file as its argument.  When the image file opens in the GUI, a left-click will plot a single new waypoint and a right-click caches
the previous series of points added.  When finished with all series of waypoints, press "enter" to output waypoints to a .txt file in the same (current directory).

The /game/race/car_sprite_images subdirectory contains a script: "_sprite_generator.py" tool.  This allows a user to easily create 360 different (1-degree increment) rotational orientation image files for a car sprite .PNG file.
To use this tool, ren the script in a cmd prompt and pass any sprite image (.PNG) file as its argument.  This will save all 360 rotated file images in the current directory.



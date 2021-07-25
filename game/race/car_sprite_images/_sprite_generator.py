import PIL as pillow
from PIL import Image
import os
import sys

# accepts full image file name as command line argument
file_name = sys.argv[1]

# Open image file
image = Image.open(file_name)

# Split file base name and extension
base_name = os.path.splitext(file_name)[0]
ext = os.path.splitext(file_name)[1]

# Rotate 1 degree at a time and save newfile
for i in range(0,360,1):
    rotated = image.rotate(-i+270, resample=0, expand=1, fillcolor="white")
    rotated.save(base_name + "_" + str(i) + ext)
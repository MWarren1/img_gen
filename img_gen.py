import random
import argparse
import numpy as np
from PIL import Image

## default settings
img_width_default       = 2000
img_height_default      = 500
img_output_file_default = "output.png"
colour_values ={
    "s" : (66, 135, 245), # Sky
    "b" : (70, 71, 70),   # Background
    "m" : (31, 97, 32),  # Midground
    "f" : (13, 158, 15),  # Foreground
    }

## CLI switches
parser = argparse.ArgumentParser(prog="img_gen", \
                                 description="Randomly generates image")
parser.add_argument("--width", required=False, \
                    help="Width of image")
parser.add_argument("--height", required=False, \
                    help="Height of image")
parser.add_argument("--output", required=False, \
                    help="filename of the output image")

args = parser.parse_args()

## Setting defaults
if args.width is None:
    img_width  = img_width_default
else:
    img_width  = args.width

if args.height is None:
    img_height = img_height_default
else:
    img_height = args.height

if args.output is None:
    img_output_file = img_output_file_default
else:
    img_output_file = args.output

def array_value_to_pixel_value(array_value, pixel_values):
    try:
        pixel_value = pixel_values[array_value]
    except:
        print("Error - No pixel value for "+str(array_value)+" in pixel_values dict")
        pixel_value = (0, 0, 0)

    return(pixel_value)

def next_height_pixel(height, last_change, image_height):
    
    change_ammount = random.randrange(1,6)
    add_or_subtract = random.randrange(1,3)

    if add_or_subtract == 1: #* subtract
        new_height = height - change_ammount
    else: #* add
        new_height = height + change_ammount

    # check if height is below zero
    if new_height < 0:
        new_height = 0

    # check if height is over image hegith
    if new_height > image_height:
        new_height = image_height
    return(new_height)

def fill_downwards(height, width, colour, image_height, image_array):
    while height < image_height:
        image_array[width, height] = colour
        height = height + 1
    width = width + 1
    return(image_array)

# create numpy array
img_array = np.full((img_width,img_height),"s", dtype=str)

#* add backgroud
print("Adding Background.........")
current_h = int(img_height/3)
current_w = 0
last_change = 0

while current_w < img_width:

    img_array = fill_downwards(current_h, current_w, "b", img_height, img_array)
    current_w = current_w + 1

    # get height of next pixel
    last_h = current_h
    current_h = next_height_pixel(current_h, last_change, img_height)
    last_change = last_h - current_h

#* adds grass
print("Adding Midground.........")
current_h = int(img_height/2)
current_w = 0
last_change = 0

while current_w < img_width:
    
    img_array = fill_downwards(current_h, current_w, "m", img_height, img_array)
    current_w = current_w + 1
    
    # get height of next pixel
    last_h = current_h
    current_h = next_height_pixel(current_h, last_change, img_height)
    last_change = last_h - current_h

#* add foreground
print("Adding Foreground.........")
current_h = int(img_height/3) * 2
current_w = 0
last_change = 0

while current_w < img_width:

    img_array = fill_downwards(current_h, current_w, "f", img_height, img_array)
    current_w = current_w + 1

    # get height of next pixel
    last_h = current_h
    current_h = next_height_pixel(current_h, last_change, img_height)
    last_change = last_h - current_h

#* below here converts image array to the output image
# creates output image
output_img = Image.new("RGB", (img_width,img_height))
print("Image Created - Width:"+str(img_width)+"  Height: "+str(img_height))

with output_img as img:
    # load pixels in to px
    px = img.load()

# convert image array to a pixel array
h_pixel = 0
while h_pixel < img_height:
    w_pixel = 0
    while w_pixel < img_width:
        #print(str(w_pixel) + " - "+ str(h_pixel))
        colour_value = array_value_to_pixel_value(img_array[w_pixel, h_pixel], colour_values)
        px[w_pixel, h_pixel] = colour_value

        w_pixel = w_pixel + 1
    h_pixel = h_pixel + 1

# save image
output_img.save(img_output_file, format="PNG")

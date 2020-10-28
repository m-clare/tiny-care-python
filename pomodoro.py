import os
import numpy
from inky import InkyPHAT
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

PATH = os.path.dirname(os.path.abspath(__file__))

# Global Inky Properties
inky_display = InkyPHAT("red")
inky_display.rotation = 0 # avoid unnecessary swap

# set start time and pomodoro cycle
start_time = 8 * 60 * 60 # seconds
pomodoro = 25 * 60 # typical length
small_break = 5 * 60
long_break = 25 * 60
cycle_length = (pomodoro + small_break) * 3 +  pomodoro + long_break

def get_pomodoro_time(curr_time):
    time_since_start = curr_time - start_time
    completed_cycles = int(time_since_start // cycle_length)
    pt_in_cycle = time_since_start - completed_cycles * cycle_length
    num_tomato = int(pt_in_cycle // (pomodoro + small_break))

    if int(pt_in_cycle % (pomodoro + small_break)  >= pomodoro) and (num_tomato < 3):
        print(num_tomato, " break time!")
    elif num_tomato == 4:
        print("long break time!")
    else:
        print(num_tomato, " still working")
        get_tomato_image(num_tomato)

def get_tomato_image(image_num):
    """
    Use PIL library to open tomato image and transpose for inky display
    """
    rel_path = os.path.join(PATH, "assets/tomato_" + str(image_num) + ".png")
    img = Image.open(rel_path).resize(inky_display.resolution)
    canvas = Image.new("P", (inky_display.rows, inky_display.cols))
    canvas.paste(img, (0,0)) # no offset of image
    canvas = canvas.transpose(Image.ROTATE_90)

    return canvas

def get_short_break_text():
    pass

def get_long_break_text():
    pass

def update_display():
    pass

# need to set that cron only refreshes the display if change in values? store values in file maybe? or better yet, only if remainder is 0?
for time in test_times:
    get_pomodoro_time(time)

# img = get_tomato_image(0)

# inky_display.set_image(img)
# inky_display.show()

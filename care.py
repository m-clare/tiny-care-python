import os
from inky import InkyWHAT
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime as dt
from twitterbot import *

PATH = os.path.dirname(os.path.abspath(__file__))

ttf = ImageFont.truetype("/Users/maryannewachter/Library/Fonts/DankMono-Italic.otf", 24)
inky_display = InkyWHAT("red")
black = inky_display.BLACK
red = inky_display.RED
white = inky_display.WHITE
inky_display.rotation = 180

def format_line(font, msg, width):
    lines = []
    w, h = font.getsize(msg)
    if w <= width:
        lines.append(msg)
    else:
        toks = msg.split()
        cur_line = ''
        for tok in toks:
            cur_w, _ = font.getsize(cur_line + tok + ' ')
            if cur_w <= width:
                cur_line = cur_line + tok + ' '
            else:
                lines.append(cur_line)
                cur_line = tok + ' '
        lines.append(cur_line)
    return lines

def get_text_image(text, width, height):
    font = ttf
    lines = format_line(font, text, width)
    _, line_height = font.getsize(lines[0])
    centered_y = (height / 2) - ((line_height * len(lines)) / 2)
    height_counter = centered_y
    img = set_blank_background(width, height)
    draw = ImageDraw.Draw(img)
    for i in range(0, len(lines)):
        msg = lines[i]
        w, h = font.getsize(msg)
        x = (width / 2) - (w / 2)
        y = height_counter
        draw.text((x, y), msg, black, font)
        height_counter += h
    return img

def set_blank_background(width, height):
    canvas = Image.new("RGB", (width, height))
    pixels = canvas.load()
    for x in range(canvas.size[0]):
        for y in range(canvas.size[1]):
            pixels[x, y] = (256, 256, 256)
    return canvas

def assemble_canvas(org, tweet, pomodoro, inky_display):
    canvas = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    # insert org
    canvas.paste(org, (0, 0)) # no offset
    # insert tweet
    canvas.paste(tweet, (org.width, 0))
    # insert pomodoro
    canvas.paste(tomato, (org.width, inky_display.HEIGHT - tomato.size[1]))
    return canvas

org_accomplishments = Image.open('./test.png')
ow, oh = org_accomplishments.size
tomato = Image.open('./assets/tomato_3.png')
tw, th = tomato.size
rem_w = inky_display.WIDTH - ow
rem_h = inky_display.HEIGHT - th
tweet = get_recent_care_tweet()
tweet_img = get_text_image(tweet, rem_w, rem_h)
org_img = org_accomplishments
canvas = assemble_canvas(org_img, tweet_img, tomato, inky_display)
# canvas.show()
inky_display.set_image(canvas)
inky_display.show()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import time
import numpy
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
from fonts.ttf import RobotoMedium
import RPi.GPIO as GPIO
from ST7789 import ST7789

SPI_SPEED_MHZ = 80

display = ST7789(
    rotation=90,  # Needed to display the right way up on Pirate Audio
    port=0,       # SPI port
    cs=1,         # SPI port Chip-select channel
    dc=9,         # BCM pin used for data/command
    backlight=13,
    spi_speed_hz=SPI_SPEED_MHZ * 1000 * 1000
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT)
FLIP = os.environ.get('FLIP', False)
WIDTH = display.height
HEIGHT = display.width
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),
    (255, 128, 0),
    (255, 255, 0),
    (128, 255, 0),
    (0, 255, 0),
    (0, 255, 128),
    (0, 255, 255),
    (0, 128, 255),
    (0, 0, 255),
    (255, 0, 255),
    (255, 0, 128),
]
index = 0

font_smiley = ImageFont.truetype('./CODE2000.TTF', 28)
font = ImageFont.truetype(RobotoMedium, 40)
img = Image.new("RGB", (WIDTH, HEIGHT), 0)
draw = ImageDraw.Draw(img)

BUTTONS = [5, 6, 16, 24]
LABELS = ['A', 'B', 'X', 'Y']
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

button = ""

def show_credits(button):
    global index
    ROTATION = 270 if FLIP else 90

    draw.text((0, 0), "A", font=font, fill=COLORS[index] if button == "A" else WHITE)
    draw.text((WIDTH - 32, 0), "X", font=font, fill=COLORS[index] if button == "X" else WHITE)
    draw.text((0, HEIGHT - 48), "B", font=font, fill=COLORS[index] if button == "B" else WHITE)
    draw.text((WIDTH - 32, HEIGHT - 48), "Y", font=font, fill=COLORS[index] if button == "Y" else WHITE)

    draw.text((int(WIDTH*0.2), int(HEIGHT*0.09)), "¯\_(ツ)_/¯", font=font_smiley, fill=COLORS[index] if button == "" else WHITE)
    draw.text((int(WIDTH*0.09), int(HEIGHT*0.35)), "promethee", font=font, fill=COLORS[index] if button == "" else WHITE)
    draw.text((int(WIDTH*0.2), int(HEIGHT*0.6)), "@github", font=font, fill=COLORS[index] if button == "" else WHITE)
    display.display(img)

def button_press(pin):
    global button
    button = LABELS[BUTTONS.index(pin)] if button == "" else ""

for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.BOTH, button_press, bouncetime=100)

while True:
    index = index + 1 if index < len(COLORS) - 1 else 0
    show_credits(button)

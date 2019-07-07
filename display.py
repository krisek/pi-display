#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pygame
from pygame import *
import os
import random
import string
import time
import ptext
import requests
from requests.packages import urllib3
import urllib
import json
import random
import beats
import sys
from signal import alarm, signal, SIGALRM, SIGKILL

from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit
import json
import configparser

config = configparser.ConfigParser()
config.read('display.ini')

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

#os.putenv('SDL_FBDEV','/dev/fb1')
#os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.environ['SDL_FBDEV'] = '/dev/fb1'
os.environ['SDL_VIDEODRIVER'] = 'fbcon'
pygame.init()
pygame.mouse.set_visible(False)
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

print("Framebuffer size: %d x %d" % (size[0], size[1]))
signal(SIGALRM, alarm_handler)
alarm(2)

try:
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    alarm(0)
except Alarm:
    raise KeyboardInterrupt

clock = pygame.time.Clock()

done = False


#font_preferences = ["freemono", "dejavuserif", "droidsansfallback", "freesans", "freeserif", "dejavusansmono", "notomono", "dejavusans"]

basicfont = pygame.font.SysFont('freesans', 30)
basicfont.set_bold(1)

temperature_timer = 0
temperature = '10'

colors = {
    'freeze': {'min': -273,
                    'max': 0,
                    'background': '#0000A6',
                    'color': '#232338'
                    },
    'cold': {'min': 0,
                    'max': 5,
                    'background': '#8484FA',
                    'color': '#232338'
                    },
    'cozy': {'min': 5,
                    'max': 10,
                    'background': '#84BCFA',
                    'color': '#232338'
                    },
     'light_green': {'min': 10,
                    'max': 18,
                    'background': '#278346',
                    'color': '#232338'
                    },
      'yellow' : {'min': 18,
                    'max': 25,
                    'background': '#DFD126',
                    'color': '#232338'
                    },
      'orange' : {'min': 25,
                    'max': 32,
                    'background': '#DF8C26',
                    'color': '#232338'
                    },
       'red' : {'min': 32,
                    'max': 100,
                    'background': '#DF8C26',
                    'color': '#232338'
                    }                               
    };
    
x=10
y=10
screen.fill(pygame.Color('#FFF6F6'))
ptext.draw("hello world", (5, size[1]-5), color="black", gcolor="green", angle=90)
pygame.display.flip()

print('entering main loop')

y_app_id = config.get('yahoo_weather', 'app_id')
y_api_key = config.get('yahoo_weather', 'api_key')
y_api_secret = config.get('yahoo_weather', 'api_secret')

#init yahoo
data = YahooWeather(APP_ID=y_app_id, api_key=y_api_key, api_secret=y_api_secret)

while not done:

    if temperature_timer == 0:
        try:
            #print('trying to get temp data')
            
            data.get_yahoo_weather_by_city("dusseldorf", Unit.celsius)
            
            
            temperature = float(data.condition.temperature())
            x = random.randint(5,size[0]-12)
            y = random.randint(25,size[1]-25)
            background = '#000000'
            color = '#ffffff'
            for color_item in colors:
                #print("{} {}".format(color_item,colors[color_item]['color'])) 
                if colors[color_item]['min'] < temperature and colors[color_item]['max'] >= temperature:
                    background = colors[color_item]['background']
                    color = colors[color_item]['color']
        except:
            print("No temperature received, let's try to reconect")
            try:
                data = YahooWeather(APP_ID=y_app_id, api_key=y_api_key, api_secret=y_api_secret)
            except:
                print("no yahoo connection")
            x=10
            y=10
            
    temperature_timer += 1
    if temperature_timer == 120:
        temperature_timer = 0
    
    #screen.fill(pygame.Color('#F6F4C1'))
    screen.fill(pygame.Color('#FFF6F6'))

    #ptext.draw(''.join(random.choice(string.ascii_uppercase + string.digits + ' ') for _ in range(42)), (10, 10), sysfontname="freesans",bold=True, fontsize=18, surf=screen, align="left",widthem=12)
    try:
        ptext.draw(" %s°C " % (round(temperature,1)), center=(x, y), sysfontname="dejavusans",bold=True, fontsize=30, surf=screen, align="center", color=color, background=background, angle=90)
    except:
        #print("color: " + color)
        print("something went wrong " + str(temperature))
        pass
    ptext.draw("%s" % (beats.now()), center=(size[0]-12,size[1]/2), sysfontname="dejavusans", fontsize=26, surf=screen, align="center", color='#000000',angle=90)
    pygame.display.flip()
    #clock.tick(15)
    time.sleep(1)

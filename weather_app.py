# Imports
import time
import urllib.parse
from tkinter import *
from PIL import Image, ImageTk
import requests
import os
import json

# Settings (later to be moved to a json config file)
#config_file = json.load('config.json')


api_key = 'd000a5219252f67b060962430f2bc72c'
zip_code = '' # if left blank, geolocation will try to get your zip code for you
refresh_time = 13  # minutes.
return_temp = 'F'  # F/C
time_format = 12  # 12/24 HR

# Geolocation -> zip
geo_url = 'http://ipinfo.io/json'
geo_json_data = requests.get(geo_url).json()
geo_zip = geo_json_data['postal']

if zip_code == '':
    zip_code = geo_zip
else:
    pass


# Openweathermap
main_api = 'http://api.openweathermap.org/data/2.5/weather?zip='
app_id = ',us&appid=' + api_key
address = zip_code
url = main_api + urllib.parse.urlencode({'address': address}) + app_id

json_data = requests.get(url).json()
current_k_temp = json_data['main']['temp']
location = json_data['name']
current_condition = json_data['weather'][0]['main']


# API hit limiter
if refresh_time < 15:
    print('Timer set below 15 minute threshold.  Setting to 15 minutes (from the currently set ' + str(refresh_time) + ' minutes).')
    refresh_time = 15
else:
    print('Timer OK')


# Status Checker
def status_checker(json_data):
    if json_data != '' :
        return True
    else:
        return False

# Time & Date Stuff
refresh_timer = refresh_time * 60

def time_now(format):
    if format == 12:
        return time.strftime("%I:%M %p")
    elif format == 24:
        return time.strftime("%H:%M")
    else:
        return time.strftime("%H:%M")


# Temp Converter
def temp_conv(current_k_temp, return_temp):
    if return_temp.lower() == 'f':
        far_temp = round((current_k_temp * 9 / 5.0) - 459.67)
        return far_temp
    elif return_temp.lower() == 'c':
        cel_temp = round(current_k_temp - 273.15)
        return cel_temp
    else:
        return current_k_temp

# Weather Image
weather_image = ''
day_night_id = ''
def weather_image_return(current_condition):
    if 'clear' in current_condition.lower():
        weather_image = os.path.join('icons', 'cog.gif')
        return weather_image
    else:
        weather_image = os.path.join('icons', 'snowflake-o.gif')
        return weather_image

    current_hour = time.strftime("%H")

    if int(current_hour) < 16:
        day_night_id = "day"
        print(day_night_id)
        return day_night_id

    elif int(current_hour) > 16:
        day_night_id = "night"

        return day_night_id

    else:
        day_night_id = "day"
        return day_night_id




# Testing Area
print(url)
#print(current_condition)
#print(weather_image)
#print(json_data['weather'][0]['main'])
#print(weather_image_return(current_condition))
#print(zip_code)
print(day_night_id)

temp = str(temp_conv(current_k_temp, return_temp))


# GUI
root = Tk()



weather_condition_image = ImageTk.PhotoImage(Image.open(weather_image_return(current_condition)))

def main_gui():

    root.wm_title("Instaweather 9000")
    current_temp = temp + '°'

    w = Canvas(root, width = 250, height = 500, bd=0, highlightthickness=0)
    w.pack()
    w.config(bg = '#444444')
    w.create_text(125, 90, font = ("Ubuntu Light", 48), text = current_temp, fill = '#ffffff')
    w.create_text(125, 125, font = ("Ubuntu Light", 10), text = location, fill = '#ffffff')
    w.create_text(125, 175, font = ("Ubuntu Light", 12), text = current_condition, fill = '#ffffff')
    w.create_image(125, 300, image = weather_condition_image)

if status_checker(json_data) == True:
    print("Connection Established")
    main_gui()
else:
    print("Unable to Connect")


root.mainloop()


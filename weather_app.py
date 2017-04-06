# Imports
import time
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import requests
import os
import logging
import json
import platform


# Config File Import
config_file_name = 'config.json'
with open(config_file_name, encoding='utf-8') as config_file:
    config = json.loads(config_file.read())

api_key = config['app_settings']['api_key']
zip_code = config['app_settings']['zip_code']
refresh_timer = config['app_settings']['refresh_timer']
return_temp = config['app_settings']['temp_format']
time_format = config['app_settings']['time_format']
api_to_use = config['app_settings']['api']
log_file_name = config['app_settings']['log_file_name']
logging_level = config['app_settings']['logging_level']


# Setups
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logging.info('Logging Enabled.')
op_sys = platform.system()
weather_return = {}



# Geolocation -> zip
geo_url = 'http://ipinfo.io/json'
geo_json_data = requests.get(geo_url).json()
geo_zip = geo_json_data['postal']
geo_loc = geo_json_data['loc']
geo_city = geo_json_data['city']


# API Key checker
'''
if api_key == '':
    api_key = input('Please enter an API key: ')
else:
    pass
'''

# ZIP code getter
if zip_code == '':
    zip_code = geo_zip
else:
    pass

def weather_api_return(api_to_use, zip_code, geo_city, return_temp):

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

    # Darksky.net
    if api_to_use == 'DS':
        ds_api = 'https://api.darksky.net/forecast/'
        ds_api_key = 'd249a10c98c1d88126495cb255b22d53'

        ds_url = ds_api + ds_api_key + '/' + geo_loc
        ds_json_data = requests.get(ds_url).json()
        location = geo_city
        current_condition = ds_json_data['currently']['summary']
        current_temp = int(ds_json_data['currently']['temperature'])
        weather_return = {'location': location, 'current_temp': current_temp, 'current_condition': current_condition}
        return weather_return


    # Openweathermap.org
    elif api_to_use == 'OWM':
        main_api = 'http://api.openweathermap.org/data/2.5/weather?zip='
        app_id = ',us&appid=' + api_key
        address = str(zip_code)
        url = main_api + address + app_id

        json_data = requests.get(url).json()
        current_k_temp = json_data['main']['temp']
        location = json_data['name']
        current_condition = json_data['weather'][0]['main']
        current_temp = temp_conv(current_k_temp, return_temp)
        weather_return = {'location': location, 'current_temp': current_temp, 'current_condition': current_condition}
        return weather_return

    else:
        if api_to_use == '':
            sys.exit(logging.error('No API Selected.'))
        else:
            sys.exit(logging.error('API Error.'))


# Time & Date Stuff
def day_night_id():
    current_hour = int(time.strftime("%H"))
    if current_hour >= 6 and current_hour < 19:
        day_night_id = "day"
    elif current_hour >= 19 or current_hour < 6:
        day_night_id = "night"
    else:
        day_night_id = "I dunno."
    return day_night_id

day_night = day_night_id()


def time_now(hr_format):
    if hr_format == 12:
        return time.strftime("%I:%M %p")
    elif hr_format == 24:
        return time.strftime("%H:%M")
    else:
        return time.strftime("%H:%M")

weather_return = weather_api_return(api_to_use, zip_code, geo_city, return_temp)

cw_condition = weather_return['current_condition']
print(cw_condition)


# Weather Image
def weather_image_return(cw_condition):
    cwc = cw_condition.lower()
    if op_sys != 'posix':
        if cwc.find("clouds") == 0 and day_night.find("night") == 0:
            weather_image = os.path.join('icons', 'nightcloudy.png')
        elif cwc.find("clouds") == 0 and day_night.find("day") == 0:
            weather_image = os.path.join('icons', 'cloudy.png')
        elif cwc.find("clear") == 0 and day_night.find("night") == 0:
            weather_image = os.path.join('icons', 'moon.png')
        elif cwc.find("clear") == 0 and day_night.find("day") == 0:
            weather_image = os.path.join('icons', 'rain.png')
        elif cwc.find("rain") == 0 and day_night.find("night") == 0:
            weather_image = os.path.join('icons', 'nightrain.png')
        elif cwc.find("rain") == 0 and day_night.find("day") == 0:
            weather_image = os.path.join('icons', 'rain.png')
        elif cwc.find("snow") == 0 and day_night.find("night") == 0:
            weather_image = os.path.join('icons', 'nightsnowing.png')
        elif cwc.find("snow") == 0 and day_night.find("day") == 0:
            weather_image = os.path.join('icons', 'snowing.png')
        elif cwc.find("mist") == 0 and day_night.find("night") == 0:
            weather_image = os.path.join('icons', 'nightwind.png')
        elif cwc.find("mist") == 0 and day_night.find("day") == 0:
            weather_image = os.path.join('icons', 'wind-1.png')
        elif cwc.find("haze") == 0 and day_night.find("night") == 0:
            weather_image = os.path.join('icons', 'nightwind.png')
        elif cwc.find("haze") == 0 and day_night.find("day") == 0:
            weather_image = os.path.join('icons', 'wind-1.png')
        else:
            logging.error("Weather Condition image for " + cwc + " not found.  Setting to default icon.")
            weather_image = os.path.join('icons', 'sun.png')
    else:
        logging.error('OS ' + op_sys + ' not found')
        weather_image = os.path.join('icons', 'cloud.png')

    return weather_image



# Testing/Junk Area
temp = str(weather_return['current_temp'])
location = str(weather_return['location'])
print(day_night)


# GUI
root = Tk()


cw_condition1 = cw_condition.lower()
weather_condition_image = weather_image_return(cw_condition1)
wci = Image.open(weather_condition_image)
wcondition_image = ImageTk.PhotoImage(wci)
current_temp = temp + '°'


# Config Page

settings_cog = os.path.join('icons', 'cog.png')
cog_img_loc = Image.open(settings_cog)
maxsize_cog = (30, 30)
cog_small_image = cog_img_loc.resize(maxsize_cog)
cog = ImageTk.PhotoImage(cog_small_image)


def config_page():

    def config_editor_button():
        if 'Windows' in op_sys:
            os.system('notepad ' + config_file_name)
        elif 'Linux' in op_sys:
            os.system('gedit ' + config_file_name)
        else:
            pass

    cp_root = Tk()
    cp = Canvas(cp_root, width=350, height=500, bd=0, highlightthickness=0)
    cp_root.resizable(width=False, height=False)
    cp_root.wm_title("Instaweather 9000.1 - Settings")
    cp.config(bg='#444444')
    cp.create_text(110, 10, font=("Segoe UI Bold", 18), text='Settings Page', fill='#ffffff')

    config_editor_button = tk.Button(cp_root, text='Edit in text editor', command=config_editor_button)
    config_editor_button.pack(side=BOTTOM)

    quit_button = tk.Button(cp_root)
    quit_button.configure(text="QUIT", command=cp_root.destroy)
    quit_button.pack(side=BOTTOM)
    cp.pack()


root.wm_title("Instaweather 9000.1")


if op_sys == 'Windows' or op_sys == 'Linux':
    root.iconphoto(True, PhotoImage(file=os.path.join('icons', 'cloud.png')))
else:
    pass #(doesn't set an app icon for OSX)

w = Canvas(root, width=250, height=500, bd=0, highlightthickness=0)
root.resizable(width=False, height=False)
w.config(bg='#444444')
w.create_image(125, 200, image=wcondition_image)

config_button = tk.Button(root, text='Settings', command=config_page)
config_button.config(image=cog, borderwidth=0, relief=SUNKEN, bg='#444444', activebackground='#444444')

w.create_text(125, 335, font=("Segoe UI Bold", 48), text=current_temp, fill='#ffffff')
w.create_text(125, 377, font=("Segoe UI", 14), text=location, fill='#ffffff')
w.create_text(125, 405, font=("Segoe UI", 18), text=cw_condition, fill='#ffffff')
w.pack()
config_button.pack(side=BOTTOM, expand=FALSE)


# Main Calls

root.mainloop()

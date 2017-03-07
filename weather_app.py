# Imports
import time
from tkinter import *
from PIL import Image, ImageTk
import requests
import os


#api_key = 'd000a5219252f67b060962430f2bc72c'
api_key = ''    # if left blank, it will request an API key
zip_code = ''  # if left blank, it will try to pull your zip code via ipinfo.io
refresh_time = 13  # minutes.
return_temp = 'F'  # F/C
time_format = 12  # 12/24 HR
api_to_use = 'OWM'  # OWM = OpenWeatherMap

# API Key checker
if api_key == '':
    api_key  = input('Please enter an API key: ')
else:
    pass

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
url = main_api + address + app_id

json_data = requests.get(url).json()
current_k_temp = json_data['main']['temp']
location = json_data['name']
current_condition = json_data['weather'][0]['main']

# API hit limiter
if refresh_time < 15:
    print('Timer set below 15 minute threshold.  Setting to 15 minutes (from the currently set ' + str(
        refresh_time) + ' minutes).')
    refresh_time = 15
else:
    print('Timer OK')


# Status Checker
def status_checker(json_data):
    if json_data != '':
        return True
    else:
        return False


# Time & Date Stuff
current_hour = int(time.strftime("%H"))
if current_hour > 16:
    day_night_id = "day"
elif current_hour < 16:
    day_night_id = "night"
else:
    print("Day/Night ID is unable to pull the current time. Setting to DAY")
    day_night_id = "day"


def time_now(hr_format):
    if hr_format == 12:
        return time.strftime("%I:%M %p")
    elif hr_format == 24:
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

def weather_image_return(current_condition):

    cwc = current_condition.lower()


    if cwc.find("clouds") == 0 and day_night_id.find("night") == 0:
        weather_image = os.path.join('icons', 'nightcloudy.png')
        return weather_image
    elif cwc.find("clouds") == 0 and day_night_id.find("day") == 0:
        weather_image = os.path.join('icons', 'cloudy.png')
        return weather_image
    elif cwc.find("clear") == 0 and day_night_id.find("night") == 0:
        weather_image = os.path.join('icons', 'moon.png')
        return weather_image
    elif cwc.find("clear") == 0 and day_night_id.find("day") == 0:
        weather_image = os.path.join('icons', 'sun.png')
        return weather_image
    elif cwc.find("rain") == 0 and day_night_id.find("night") == 0:
        weather_image = os.path.join('icons', 'nightrain.png')
        return weather_image
    elif cwc.find("rain") == 0 and day_night_id.find("day") == 0:
        weather_image = os.path.join('icons', 'rain.png')
        return weather_image
    elif cwc.find("snow") == 0 and day_night_id.find("night") == 0:
        weather_image = os.path.join('icons', 'nightsnowing.png')
        return weather_image
    elif cwc.find("snow") == 0 and day_night_id.find("day") == 0:
        weather_image = os.path.join('icons', 'snowing.png')
        return weather_image
    else:
        print("Weather Condition image for " + cwc + " not found.  Setting to default icon.")
        weather_image = os.path.join('icons', 'sun.png')
        return weather_image


# Testing Area

print(url)
print("Image to show : " + weather_image_return(current_condition))

temp = str(temp_conv(current_k_temp, return_temp))

# GUI
root = Tk()

weather_condition_image = ImageTk.PhotoImage(Image.open(weather_image_return(current_condition)))


def main_gui():
    root.wm_title("Instaweather 9000")
    current_temp = temp + '°'

    w = Canvas(root, width=250, height=500, bd=0, highlightthickness=0)
    w.pack()
    w.config(bg='#444444')
    w.create_text(125, 90, font=("Ubuntu Light", 48), text=current_temp, fill='#ffffff')
    w.create_text(125, 125, font=("Ubuntu Light", 10), text=location, fill='#ffffff')
    w.create_text(125, 175, font=("Ubuntu Light", 12), text=current_condition, fill='#ffffff')
    w.create_image(125, 300, image=weather_condition_image)


if status_checker(json_data) == True:
    print("Connection Established")
    main_gui()
else:
    print("Unable to Connect")

root.mainloop()

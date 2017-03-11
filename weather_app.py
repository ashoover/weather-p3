# Imports
import time
from tkinter import *
from PIL import Image, ImageTk
import requests
import os
import logging


api_key = 'd000a5219252f67b060962430f2bc72c'    # if left blank, it will request an API key the user
zip_code = '36575'  # if left blank, it will attempt to pull your zip code via ipinfo.io
refresh_time = 13  # if less than 15 mins, it will change this value
return_temp = 'F'  # F/C
time_format = 12  # 12/24 HR
api_to_use = 'OWM'  # OWM = OpenWeatherMap / DS = DarkSky / AW = AccuWeather / WU = WeatherUnderground
log_file_name = 'log.txt'
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
weather_return = {}


# Geolocation -> zip
geo_url = 'http://ipinfo.io/json'
geo_json_data = requests.get(geo_url).json()
geo_zip = geo_json_data['postal']
geo_loc = geo_json_data['loc']
geo_city = geo_json_data['city']


# API Key checker
if api_key == '':
    api_key = input('Please enter an API key: ')
else:
    pass


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
        logging.info('Using the DarkSky API')


    # Openweathermap.org
    elif api_to_use == 'OWM':
        main_api = 'http://api.openweathermap.org/data/2.5/weather?zip='
        app_id = ',us&appid=' + api_key
        address = zip_code
        url = main_api + address + app_id

        json_data = requests.get(url).json()
        current_k_temp = json_data['main']['temp']
        location = json_data['name']
        current_condition = json_data['weather'][0]['main']
        current_temp = temp_conv(current_k_temp, return_temp)
        weather_return = {'location': location, 'current_temp': current_temp, 'current_condition': current_condition}
        return weather_return
        logging.info('Using the OpenWeatherMap API')

    else:
        if api_to_use == '':
            sys.exit(logging.error('No API Selected.'))
        else:
            sys.exit(logging.error('API Error (incorrect key?).'))


# Time & Date Stuff
def day_night_id():
    current_hour = int(time.strftime("%H"))
    if 6 >= current_hour < 19:
        day_night_id = "day"
    elif current_hour >= 19:
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
print(weather_return)
cw_condition = weather_return['current_condition']
print(cw_condition)


# Weather Image
def weather_image_return(cw_condition: object) -> object:
    cwc = cw_condition.lower()
    if cwc.find("clouds") == 0 and day_night.find("night") == 0:
        weather_image = os.path.join('icons', 'nightcloudy.png')
        return weather_image
    elif cwc.find("clouds") == 0 and day_night.find("day") == 0:
        weather_image = os.path.join('icons', 'cloudy.png')
        return weather_image
    elif cwc.find("clear") == 0 and day_night.find("night") == 0:
        weather_image = os.path.join('icons', 'moon.png')
        return weather_image
    elif cwc.find("clear") == 0 and day_night.find("day") == 0:
        weather_image = os.path.join('icons', 'sun.png')
        return weather_image
    elif cwc.find("rain") == 0 and day_night.find("night") == 0:
        weather_image = os.path.join('icons', 'nightrain.png')
        return weather_image
    elif cwc.find("rain") == 0 and day_night.find("day") == 0:
        weather_image = os.path.join('icons', 'rain.png')
        return weather_image
    elif cwc.find("snow") == 0 and day_night.find("night") == 0:
        weather_image = os.path.join('icons', 'nightsnowing.png')
        return weather_image
    elif cwc.find("snow") == 0 and day_night.find("day") == 0:
        weather_image = os.path.join('icons', 'snowing.png')
        return weather_image
    elif cwc.find("mist") == 0 and day_night.find("night") == 0:
        weather_image = os.path.join('icons', 'nightwind.png')
        return weather_image
    elif cwc.find("mist") == 0 and day_night.find("day") == 0:
        weather_image = os.path.join('icons', 'wind-1.png')
        return weather_image
    else:
        logging.error("Weather Condition image for " + cwc + " not found.  Setting to default icon.")
        weather_image = os.path.join('icons', 'sun.png')
        return weather_image


# Testing/Junk Area
temp = str(weather_return['current_temp'])
location = str(weather_return['location'])




# GUI
root = Tk()

#def main_gui():

cw_condition1 = cw_condition.lower()
weather_condition_image = weather_image_return(cw_condition1)
print(weather_condition_image)
wci = Image.open(weather_condition_image)
wcondition_image = ImageTk.PhotoImage(wci)

root.wm_title("Instaweather 9000")
root.iconphoto(True, PhotoImage(file=os.path.join('icons', 'cloud.png')))

current_temp = temp + '°'

w = Canvas(root, width=250, height=500, bd=0, highlightthickness=0)
w.pack()
w.config(bg='#444444')
w.create_text(125, 90, font=("Ubuntu Light", 48), text=current_temp, fill='#ffffff')
w.create_text(125, 135, font=("Ubuntu Light", 10), text=location, fill='#ffffff')
w.create_text(125, 175, font=("Ubuntu Light", 12), text=cw_condition, fill='#ffffff')
w.create_image(125, 300, image=wcondition_image)


# Main Calls
#main_gui()
root.mainloop()

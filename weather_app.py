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
from types import *


# Config File Import
config_file_name = "config.json"
with open(config_file_name, encoding="utf-8") as config_file:
    config = json.loads(config_file.read())

api_key = config["app_settings"]["api_key"]
zip_code = config["app_settings"]["zip_code"]
refresh_timer = config["app_settings"]["refresh_timer"]
return_temp = config["app_settings"]["temp_format"]
time_format = config["app_settings"]["time_format"]
api_to_use = config["app_settings"]["api"]
log_file_name = config["app_settings"]["log_file_name"]
logging_level = config["app_settings"]["logging_level"]
regular_font = config["appearance"]["font"]
bold_font = config["appearance"]["bold_font"]
background_color = config["appearance"]["bg_color"]
last_checked_notif = config["appearance"]["last_checked_notif"]
offline_mode = config["data"]["offline_mode"]
bg_color = background_color
app_lvl = config["app_settings"]["app_level"]


# Setups
logging.basicConfig(filename=log_file_name, level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logging.info("Logging Enabled.")
op_sys = platform.system()
weather_return = {}


# Refresh timer limit
if int(refresh_timer) < 14:
    refresh_timer = 15
    logging.info("Refresh time set below 15 minute limit.  Setting to 15 minutes.")
else:
    pass


# Geolocation -> zip
geo_url = "http://ipinfo.io/json"
geo_json_data = requests.get(geo_url).json()
geo_zip = geo_json_data["postal"]
geo_loc = geo_json_data["loc"]
geo_city = geo_json_data["city"]


# ZIP code getter
if zip_code == "":
    zip_code = geo_zip
    logging.info('No ZIP code found in the config.  Using ' + zip_code)
else:
    pass

def weather_api_return(api_to_use, zip_code, geo_city, return_temp):

    # Temp Converter
    def temp_conv(current_k_temp, return_temp):
        if return_temp.lower() == "f":
            far_temp = round((current_k_temp * 9 / 5.0) - 459.67)
            return far_temp
        elif return_temp.lower() == "c":
            cel_temp = round(current_k_temp - 273.15)
            return cel_temp
        else:
            return current_k_temp

    # Darksky.net
    if api_to_use == "DS":
        ds_api = "https://api.darksky.net/forecast/"
        url = ds_api + api_key + "/" + geo_loc
        logging.info(url)

        ds_json_data = requests.get(url).json()
        location = geo_city
        current_condition = ds_json_data["currently"]["summary"]
        current_temp = int(ds_json_data["currently"]["temperature"])
        weather_return = {"location": location, "current_temp": current_temp, "current_condition": current_condition}
        return weather_return


    # Openweathermap.org
    elif api_to_use == "OWM":
        main_api = "http://api.openweathermap.org/data/2.5/weather?zip="
        app_id = ",us&appid=" + api_key
        address = str(zip_code)
        url = main_api + address + app_id
        logging.info(url)

        json_data = requests.get(url).json()
        current_k_temp = json_data["main"]["temp"]
        location = json_data["name"]
        current_condition = json_data["weather"][0]["main"]
        current_temp = temp_conv(current_k_temp, return_temp)
        weather_return = {"location": location, "current_temp": current_temp, "current_condition": current_condition}
        return weather_return

    elif api_to_use == "WU":
        pass

    else:
        if api_to_use == "":
            sys.exit(logging.error('No API selected.'))
        else:
            sys.exit(logging.error('No API "' + api_to_use + '" found.'))


# Time & Date Stuff
def day_night_id():
    current_hour = int(time.strftime("%H"))
    if current_hour >= 6 and current_hour < 19:
        day_night_id = "day"
    elif current_hour >= 19 or current_hour < 6:
        day_night_id = "night"
    else:
        day_night_id = "day"
        logging.ERROR('Day/Night ID not detected.')
    return day_night_id

day_night = day_night_id()


def time_now(hr_format):
    if hr_format == 12:
        return time.strftime("%I:%M %p")
    elif hr_format == 24:
        return time.strftime("%H:%M")
    else:
        return time.strftime("%H:%M")

time_right_meow = time_now(time_format)



weather_return1 = weather_api_return(api_to_use, zip_code, geo_city, return_temp)
temp = str(weather_return1["current_temp"])
location = str(weather_return1["location"])
cw_condition = weather_return1["current_condition"]
current_temp = temp + "°"


if app_lvl == "G":
    logging.info("Running GUI version only.")

    # Weather Image

    def weather_image_return(cw_condition):
        cwc = cw_condition.lower()
        if op_sys != "posix":
            if cwc.find("clouds") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "nightcloudy.png")
            elif cwc.find("clouds") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "cloudy.png")
            elif cwc.find("cloudy") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "cloudy.png")
            elif cwc.find("cloudy") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "nightcloudy.png")
            elif cwc.find("clear") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "moon.png")
            elif cwc.find("clear") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "sun.png")
            elif cwc.find("rain") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "nightrain.png")
            elif cwc.find("rain") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "rain.png")
            elif cwc.find("snow") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "nightsnowing.png")
            elif cwc.find("snow") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "snowing.png")
            elif cwc.find("mist") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "nightwind.png")
            elif cwc.find("mist") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "wind-1.png")
            elif cwc.find("haze") != -1 and day_night.find("night") != -1:
                weather_image = os.path.join("icons", "nightwind.png")
            elif cwc.find("haze") != -1 and day_night.find("day") != -1:
                weather_image = os.path.join("icons", "wind-1.png")
            else:
                logging.error("Weather Condition image for " + cwc + " not found.  Setting to default icon.")
                weather_image = os.path.join("icons", "sun.png")
        else:
            logging.error("OS " + op_sys + " not found")
            weather_image = os.path.join("icons", "cloud.png")

        return weather_image

    # GUI Setup
    cw_condition1 = cw_condition.lower()

    # Last Checked Notification
    def last_checked():
        if last_checked_notif:
            checked_time = "Last checked at " + time_right_meow
            w.create_text(125, 460, font=(regular_font, 7), text=checked_time, fill="#ffffff")
        else:
            pass

    root = Tk()

    weather_condition_image = weather_image_return(cw_condition1)
    wci = Image.open(weather_condition_image)
    wcondition_image = ImageTk.PhotoImage(wci)

    # Config Page
    settings_cog = os.path.join("icons", "settings.png")
    cog_img_loc = Image.open(settings_cog)
    maxsize_cog = (30, 30)
    cog_small_image = cog_img_loc.resize(maxsize_cog)
    cog = ImageTk.PhotoImage(cog_small_image)

    def config_page():
        cp_root = Tk()
        cp_root.config(bd=0, width=500, height=500, highlightthickness=0)
        cp_root.resizable(width=False, height=False)
        cp_root.attributes("-topmost", True)
        cp_root.wm_title("Settings")
        cp_root.geometry("500x500")
        #cp_root.config(bg=bg_color)

        api_radio = StringVar().set(api_to_use)
        c_zip_code = StringVar(cp_root, value=zip_code)
        c_api_key = StringVar(cp_root, value=api_key)
        c_refresh_timer = StringVar(cp_root, value=refresh_timer)
        c_logging_level = StringVar(cp_root, value=logging_level)
        c_time_format = StringVar(cp_root, value=time_format)

        # Field Labels
        zip_label = Label(cp_root, text="Zip Code ")
        api_label = Label(cp_root, text="API ")
        api_key_label = Label(cp_root, text="API Key ")
        refresh_timer_label = Label(cp_root, text="Refresh Timer in M ")
        logging_level_label = Label(cp_root, text="Logging Level ")
        time_format_label = Label(cp_root, text="Time Format ")

        # Entry Fields
        zip_code_entry = Entry(cp_root, textvariable=c_zip_code)
        api_radio_1 = Radiobutton(cp_root, text="OpenWeatherMap", variable=api_radio, value="OWM")
        api_radio_2 = Radiobutton(cp_root, text="DarkSky", variable=api_radio, value="DS")
        api_key_entry = Entry(cp_root, textvariable=c_api_key, width=30)
        refresh_timer_entry = Entry(cp_root, textvariable=c_refresh_timer)
        logging_level_entry = Entry(cp_root, textvariable=c_logging_level)
        time_format_entry = Entry(cp_root, textvariable=c_time_format)

        # Grid Layout
        zip_label.grid(row=0, sticky='e')
        api_label.grid(row=1, sticky='e')
        api_key_label.grid(row=2, sticky='e')
        refresh_timer_label.grid(row=3, sticky='e')
        logging_level_label.grid(row=4, sticky='e')
        time_format_label.grid(row=5, sticky='e')
        zip_code_entry.grid(row=0, column=1)
        api_radio_1.grid(row=1, column=1)
        api_radio_2.grid(row=1, column=2)
        api_key_entry.grid(row=2, column=1, columnspan=2, sticky='we')
        refresh_timer_entry.grid(row=3, column=1)
        logging_level_entry.grid(row=4, column=1)
        time_format_entry.grid(row=5, column=1)

        cp_root.mainloop()

    root.wm_title("Instaweather 9000.1")


    if op_sys == "Windows" or op_sys == "Linux":
        root.iconphoto(True, PhotoImage(file=os.path.join("icons", "cloud.png")))
    else:
        pass #(doesn't set an app icon for OSX)

    w = Canvas(root, width=250, height=500, bd=0, highlightthickness=0)
    root.resizable(width=False, height=False)
    w.config(bg=bg_color)
    w.create_image(125, 150, image=wcondition_image)

    config_button = tk.Button(root, text="Settings", command=config_page)
    config_button.config(image=cog, borderwidth=0, relief=SUNKEN, bg=bg_color, activebackground=bg_color)

    w.create_text(125, 335, font=(bold_font, 48), text=current_temp, fill="#ffffff")
    w.create_text(125, 377, font=(regular_font, 14), text=location, fill="#ffffff")
    w.create_text(125, 405, font=(regular_font, 18), text=cw_condition, fill="#ffffff")
    w.pack()
    last_checked()
    config_button.pack(side=RIGHT, fill=X, expand=True)

    # Main Calls
    root.mainloop()

elif app_lvl == "C":
    def console_app():
        # Console Version
        console_weather = current_temp + "F in " + location + " and " + cw_condition + '.'

        lcn = eval(last_checked_notif)
        
        def last_checked(lcn):
            if lcn == 'True':
                return("Last checked at " + time_right_meow + "\n")
            else:
                return("")
            
        def blah():                
            print("")
            print("===== Current Weather =====")
            print("")
            print(console_weather)
            print(last_checked(last_checked_notif))
            print("===========================")
            print("")
        
        while True:
            if os.name == 'nt':
                os.system('cls')
            else:
                os.system('clear')
                
            blah()
            time.sleep(15)

    console_app()

else:
    logging.error("Invalid App Lvl")



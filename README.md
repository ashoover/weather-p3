weather-p3


config.json --

{
    "appearance":
        {
            "theme": "dark",  -- light/dark
            "font": "Verdana",
            "bold_font": "Verdana Bold",
            "bg_color": "gray27", -- https://goo.gl/gtPSCg
            "last_checked_notif": "True" -- show the last time it hit the api
        },
    "app_settings":
        {
            "zip_code": "36575", -- can be left blank
            "api_key": "d249a10c98c1d88126495cb255b22d53",
            "owm_api_key": "d000a5219252f67b060962430f2bc72c",  -- not used
            "api": "DS", -- OWM/DS
            "refresh_timer": 13, -- will be ignored if set below 15
            "temp_format": "F", -- F/C
            "time_format": 12, -- 12/24
            "log_file_name": "log.txt",  --
            "logging_level": "logging.INFO",  -- python logging module mode
            "app_level": "G" -- G/C (G = GUI, C = Console)
        },
    "data":
        {
            "offline_mode" : "False",
            "database_name" : "weather_app.db"
        }
}
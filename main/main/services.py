from pprint import pprint
from functools import lru_cache
from timezonefinder import TimezoneFinder
import requests
import datetime
import geocoder

#geocoder function to get infos from user
@lru_cache
def get_user_info():
     g = geocoder.ip('me')
     latitude, longitude = g.latlng
     user_language = g.country

     timezone_finder = TimezoneFinder()
     user_timezone = timezone_finder.timezone_at(lat=latitude, lng=longitude)
     user_infos = {"language" : user_language, "timezone" : user_timezone}
     return user_infos

# function to call in re.sub
def make_link(match):
    url = match.group(0)
    return f'<br><a href="{url}" target="_blank">{url}</a>'

#get current weather conditions from API
@lru_cache
def get_weather(city, key, lang):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang={lang}'
        weather_data = requests.get(request_url).json()
        return weather_data

# get forecast info from API
@lru_cache
def get_forecast_weather(lat, lon, key, lang):
     request_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,current&appid={key}&units=metric&lang={lang}'
     forecast_data = requests.get(request_url).json()
     pprint(forecast_data)
     return(forecast_data)

# timestamp to readable date
def unix_converter(timestamp, date_format):
     dt_object = datetime.datetime.fromtimestamp(timestamp)

     if date_format == "date":
          readable_date = dt_object.strftime("%A %d/%m/%Y")
     else:
         readable_date = dt_object.strftime("%H:%M")

     return readable_date

# treanslate text to italian we could add a paramater to translate from geo infos of user
def translate(translator, text, lang):
     translation = translator.translate(text, dest=lang)
     return translation.text

from functools import lru_cache
from googletrans import Translator
from timezonefinder import TimezoneFinder
import datetime
import geocoder
import json
import requests
import re

#geocoder function to get info from user
@lru_cache
def get_user_info() -> dict:
     g = geocoder.ip('me')
     latitude, longitude = g.latlng
     user_language = g.country

     user_timezone = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
     user_info = {"language" : user_language, "timezone" : user_timezone}
     return user_info

# function to call in re.sub
def make_link(match:re.Match[str]) -> str:
    url = match.group(0)
    return f'<a href="{url}" target="_blank">{url}</a>'

# get current weather conditions from API
@lru_cache
def get_weather(city:str, key:str, lang:str) -> dict|bool:
        
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang={lang}'
        weather_data = requests.get(request_url).json()
        status_code = weather_data['cod']
        
        if status_code == 200:
          return weather_data
        
        return False

# get current general air conditions of the zone
@lru_cache
def get_air_condition(lat, lon, key, lang:str) -> dict|int:
     url = f'https://airquality.googleapis.com/v1/currentConditions:lookup?key={key}'

     payload = {
     "location": {
          "latitude": lat,
          "longitude": lon
     },
     "extraComputations": [
          "DOMINANT_POLLUTANT_CONCENTRATION",
          "POLLUTANT_CONCENTRATION",
          "LOCAL_AQI",
     ],
     "languageCode": lang
     }

     headers = {
     'Content-Type': 'application/json'
     }

     response = requests.post(url, headers=headers, data=json.dumps(payload))

     if response.status_code == 200:
          air_conditions = response.json()
          return air_conditions

     return response.status_code

# get forecast info from API
@lru_cache
def get_forecast_weather(lat, lon, key:str, lang:str) -> dict:

     request_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,current&appid={key}&units=metric&lang={lang}'
     forecast_data = requests.get(request_url).json()
     
     return forecast_data

'''
this function converts a unix timestamp in the desired human-readable format
it takes as an argument the timestamp to be converted and the format you want it to
be returned in. You can simply pass in date_format="date".
'''
def unix_timestamp_converter(timestamp:int, date_format:str='') -> str:
     dt_object = datetime.datetime.fromtimestamp(timestamp)

     if date_format == "date":
          readable_date = dt_object.strftime("%A %d/%m/%Y")
     else:
         readable_date = dt_object.strftime("%H:%M")

     return readable_date

'''
this function takes as arguments a translator object from googletrans, 
the text to be translated and the lang for which you want the text to be returned in
you can get the user language dinamically by simly importing it from the settings file
'''
def translate(translator:Translator, text:str, lang:str) -> str:
     translation = translator.translate(text, dest=lang)
     return translation.text

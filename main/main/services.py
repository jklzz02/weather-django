from pprint import pprint
from functools import lru_cache
from timezonefinder import TimezoneFinder
import requests
import datetime
import geocoder
import json

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

@lru_cache
def get_air_condition(lat, lon, key, lang):
     url = f'https://airquality.googleapis.com/v1/currentConditions:lookup?key={key}'

     payload = {
     "universalAqi": True,
     "location": {
          "latitude": lat,
          "longitude": lon
     },
     "extraComputations": [
          "HEALTH_RECOMMENDATIONS",
          "DOMINANT_POLLUTANT_CONCENTRATION",
          "POLLUTANT_CONCENTRATION",
          "LOCAL_AQI",
          "POLLUTANT_ADDITIONAL_INFO"
     ],
     "languageCode": lang
     }

     headers = {
     'Content-Type': 'application/json'
     }

     response = requests.post(url, headers=headers, data=json.dumps(payload))
     air_conditions = response.json()

     return json.dumps(air_conditions, indent=3)

# get forecast info from API
@lru_cache
def get_forecast_weather(lat, lon, key, lang):
     request_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,current&appid={key}&units=metric&lang={lang}'
     forecast_data = requests.get(request_url).json()
     return(forecast_data)

'''
this function converts a unix timestamp in the desired human-readable format
it takes as an argument the timestamp to be converted and the format you want it to
be returned in. You can simply pass in date_format="date".
'''
def unix_timestamp_converter(timestamp, date_format):
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
def translate(translator, text, lang):
     translation = translator.translate(text, dest=lang)
     return translation.text

from functools import lru_cache
from django.conf import settings
from .utilities import get_request, post_request

lang = settings.LANGUAGE_CODE

__weather_key = settings.KEYS['weather_key']
__air_key = settings.KEYS['air_key']
__open_weather = 'https://api.openweathermap.org'
__google_aqi = 'https://airquality.googleapis.com'

@lru_cache
def get_current_weather(city:str, lang:str=lang) -> dict|bool:
    url = f'{__open_weather}/data/2.5/weather'
    params = {
            'appid' : __weather_key,
            'q' : city,
            'units' : 'metric',
            'lang' : lang
    }

    current_weather = get_request(url, params)
    return current_weather

@lru_cache
def get_forecast_weather(lat:str, lon:str, lang:str=lang) -> dict|bool:
    url = f'{__open_weather}/data/3.0/onecall'
    params = {
            'lat' : lat,
            'lon' : lon,
            'appid' : __weather_key,
            'lang' : lang
    }
       
    forecast_data = get_request(url, params)
    return forecast_data

@lru_cache
def get_air_conditions(lat:str, lon:str, lang:str=lang) -> dict|bool:

    url = f'{__google_aqi}/v1/currentConditions:lookup'
    params = {"key" : __air_key}
    json = {
        "location":
          {
            "latitude": lat,
           "longitude": lon
           },
            "extraComputations": [
                "DOMINANT_POLLUTANT_CONCENTRATION",
                "POLLUTANT_CONCENTRATION",
                "LOCAL_AQI",
            ],
            "languageCode": lang,
        }
        
    air_conditions = post_request(url, params, json)
    return air_conditions
    
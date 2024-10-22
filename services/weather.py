from aiocache import cached
from django.conf import settings
from typing import Optional
from .utilities import request

lang = settings.LANGUAGE_CODE

__weather_key = settings.KEYS['weather_key']
__air_key = settings.KEYS['air_key']
__open_weather = 'https://api.openweathermap.org'
__google_aqi = 'https://airquality.googleapis.com'

@cached(ttl=180) # cache expires in 2 min
async def get_current_weather(city: str="", lat: str="", lon: str="", lang: str=lang) -> Optional[dict]:
    url = f'{__open_weather}/data/2.5/weather'
    params = {
        'appid': __weather_key,
        'q': city,
        'units': 'metric',
        'lat' : lat,
        'lon' : lon,
        'lang': lang
    }
    return await request(url, params)

@cached(ttl=180)
async def get_forecast_weather(lat: str, lon: str, lang: str=lang) -> Optional[dict]:
    url = f'{__open_weather}/data/3.0/onecall'
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': __weather_key,
        'lang': lang
    }
    return await request(url, params)

@cached(ttl=180)
async def get_air_conditions(lat: str, lon: str, lang: str=lang) -> Optional[dict]:
    url = f'{__google_aqi}/v1/currentConditions:lookup'
    params = {"key": __air_key}
    json = {
        "location": {
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
    return await request(url, params, json, method="POST")
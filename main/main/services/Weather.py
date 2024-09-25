from dotenv import load_dotenv
from functools import lru_cache
from json import dumps
from os import getenv
from requests import get as get_request, post as post_request
from urllib.parse import urlencode

load_dotenv()
key = getenv("API_KEY")
air_key = getenv("AIR_KEY")
map_key = getenv("MAP_KEY")

class Weather:
    __open_weather = 'https://api.openweathermap.org/data/'
    __google_aqi = 'https://airquality.googleapis.com/'
    __key = key
    __air_key = air_key
    __map_key = map_key

    @lru_cache
    def current(self, city:str, lang:str) -> dict|bool:

        endpoint = '2.5/weather'
        params = {
            'appid' : self.__key,
            'q' : city,
            'units' : 'metric',
            'lang' : lang
        }

        request_url = self.__build_url(self.__open_weather, endpoint, params)

        weather_data = get_request(request_url).json()

        status_code = weather_data['cod']
        
        if not status_code == 200:    
            return False
        
        return weather_data
    
    @lru_cache
    def forecast(self, lat:str, lon:str, lang:str) -> dict|bool:

        endpoint = '3.0/onecall'
        params = {
            'lat' : lat,
            'lon' : lon,
            'appid' : self.__key,
            'lang' : lang
        }
       
        request_url = self.__build_url(self.__open_weather, endpoint, params)

        forecast_data = get_request(request_url).json()

        if forecast_data.get('cod'):
            return False

        return forecast_data
    
    @lru_cache
    def air_condition(self, lat:str, lon:str, lang:str) -> dict|bool:

        endpoint = 'v1/currentConditions:lookup'
        params = {'key' : self.__air_key} 

        request_url = self.__build_url(self.__google_aqi, endpoint, params)

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

        response = post_request(request_url, headers=headers, data=dumps(payload))

        if not response.status_code == 200:
            return False
        
        air_conditions = response.json()
        return air_conditions
    
    def map(self) -> str:
        return self.__map_key
    
    def __build_url(self, base:str, endpoint: str, params: dict) -> str:

        return f"{base}{endpoint}?{urlencode(params)}"
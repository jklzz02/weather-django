from functools import lru_cache
from json import dumps
from .RequestHelper import RequestHelper

class Weather:

    def __init__(self, RequestHelper:RequestHelper, weather_key:str, air_key:str) -> None:
        self.__open_weather = 'https://api.openweathermap.org/'
        self.__google_aqi = 'https://airquality.googleapis.com/'
        self.__weather_key = weather_key
        self.__air_key = air_key
        self.__request = RequestHelper

    @lru_cache
    def current(self, city:str, lang:str) -> dict|bool:

        endpoint = 'data/2.5/weather'
        params = {
            'appid' : self.__weather_key,
            'q' : city,
            'units' : 'metric',
            'lang' : lang
        }

        request_url = self.__request.build_url(self.__open_weather, endpoint, params)
        current_weather = self.__request.get(request_url)
        return current_weather
    
    @lru_cache
    def forecast(self, lat:str, lon:str, lang:str) -> dict|bool:

        endpoint = 'data/3.0/onecall'
        params = {
            'lat' : lat,
            'lon' : lon,
            'appid' : self.__weather_key,
            'lang' : lang
        }
       
        request_url = self.__request.build_url(self.__open_weather, endpoint, params)

        forecast_data = self.__request.get(request_url)
        return forecast_data

    @lru_cache
    def air_condition(self, lat:str, lon:str, lang:str) -> dict|bool:

        endpoint = 'v1/currentConditions:lookup'
        params = {'key' : self.__air_key} 

        request_url = self.__request.build_url(self.__google_aqi, endpoint, params)

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

        air_conditions = self.__request.post(request_url, headers=headers, data=dumps(payload))

        return air_conditions
    
    @lru_cache
    def geo_code(self, city:str, state_code:str='', country_code:str='') -> dict|bool:

        query = f"{city},{state_code},{country_code}".strip(',')

        endpoint = "geo/1.0/direct"
        params = {
            'q' : query,
            'appid' : self.__weather_key

        }

        request_url = self.__request.build_url(self.__open_weather, endpoint, params)
        response = self.__request.get(request_url)

        if not response:
            return False

        coord = {
            'lat' : response[0]['lat'],
            'lon' : response[0]['lon']
        }
        
        return coord
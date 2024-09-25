from dotenv import load_dotenv
from functools import lru_cache
from os import getenv
from requests import get, post
import json

load_dotenv()
key = getenv("API_KEY")
air_key = getenv("AIR_KEY")
map_key = getenv("MAP_KEY")

class Weather:
    __key = key
    __air_key = air_key
    __map_key = map_key

    @lru_cache
    def current(self, city:str, lang:str) -> dict|bool:

        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={self.__key}&q={city}&units=metric&lang={lang}'
        weather_data = get(request_url).json()
        status_code = weather_data['cod']
        
        if status_code == 200:
          return weather_data
        
        return False
    
    @lru_cache
    def forecast(self, lat:str, lon:str, lang:str) -> dict:
       
        request_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,current&appid={self.__key}&units=metric&lang={lang}'
        forecast_data = get(request_url).json()
     
        return forecast_data
    
    @lru_cache
    def air_condition(self, lat:str, lon:str, lang:str) -> dict|int:
        url = f'https://airquality.googleapis.com/v1/currentConditions:lookup?key={self.__air_key}'

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

        response = post(url, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            air_conditions = response.json()
            return air_conditions

        return response.status_code
    
    def map(self):
        return self.__map_key
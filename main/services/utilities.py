from geocoder import ip
from os import getenv
from functools import lru_cache
from timezonefinder import TimezoneFinder


# geocoder function to get info from user ip
@lru_cache
def get_user_info() -> dict:
     g = ip('me')
     latitude, longitude = g.latlng
     user_language = g.country

     user_timezone = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
     user_info = {"language" : user_language, "timezone" : user_timezone}
     return user_info


'''
tries to load env variable, raises Valuerror if it fails.
'''
def getenvOrFail(key:str) -> str:

     value = getenv(key)

     if value is None or value == "":
          raise ValueError(f"No env variable found for '{key}'")
     
     return value
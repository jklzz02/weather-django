from geocoder import ip
from timezonefinder import TimezoneFinder

# geocoder function to get info from user ip
def get_user_info() -> dict:
     g = ip('me')
     latitude, longitude = g.latlng
     user_language = g.country

     user_timezone = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
     user_info = {"language" : user_language, "timezone" : user_timezone}
     return user_info
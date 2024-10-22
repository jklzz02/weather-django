from asgiref.sync import sync_to_async
from .models import City
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from fuzzywuzzy import process
from services.utilities import make_link, unix_timestamp_converter
from services.weather import get_current_weather, get_forecast_weather, get_air_conditions
from typing import Optional, Tuple, List
import asyncio
import re

@sync_to_async
def get_cities_starting_with(user_input: str) -> List[str]:
    return list(City.objects.filter(name__istartswith=user_input[0]).values_list('name', flat=True))

async def suggest_city(user_input :str) -> Optional[dict]:
    if not user_input:
        return []

    cities = await get_cities_starting_with(user_input)

    if not cities:
        return []

    suggestions = process.extract(user_input, cities, limit=3)
    return [s[0] for s in suggestions]

async def home(request):
    
    async def get_cities_info() -> Optional[list]:
     start_cities = ["turin, it", "rome, it", "florence, it", "naples, it", "milan, it"]
     return await asyncio.gather(*(get_current_weather(city) for city in start_cities))
    
    start_cities_info = await get_cities_info()

    return render(request, "home.html", {"start_cities_info" : start_cities_info})

async def city(request):
     city_info = ""  
     forecast_weather = "" 
     alert = ""
     air_conditions = {}
     forecast_info = [] 
     hourly_forecast = []
     error = False

     city = request.GET.get("city")

     if city is None or not city.strip():
          referer = request.META.get('HTTP_REFERER')
          return HttpResponseRedirect(referer if referer else reverse("home"))

     formatted_date = datetime.now().strftime('%d/%m/%Y %H:%M')

     async def weather_info() -> Optional[Tuple[dict, dict, dict]]:
          city_info = await get_current_weather(city)
          
          if city_info:
               lat = city_info['coord']['lat']
               lon = city_info['coord']['lon']

               forecast_weather, air_conditions = await asyncio.gather(
                    get_forecast_weather(lat, lon),
                    get_air_conditions(lat, lon)
               )

               return city_info, forecast_weather, air_conditions
          
          return None, None, None
          
     city_info, forecast_weather, raw_air_conditions = await weather_info()


     if not city_info or not forecast_weather:

          suggestions = await suggest_city(city)
          return render(request, "city.html", {"city" : city, "suggestions" : suggestions, "error" : True})
        
     if raw_air_conditions:
          air_conditions["aqi"] = raw_air_conditions["indexes"][0]["aqiDisplay"]

          if int(air_conditions["aqi"]) < 50:
               color = "green";
          elif int(air_conditions["aqi"]) < 100:
               color = "yellow"
          else:
               color = "red"

          air_conditions["aqi_color"] = color
          air_conditions["category"] = raw_air_conditions["indexes"][0]["category"]
          air_conditions["dominant_pollutant"] = raw_air_conditions["indexes"][0]["dominantPollutant"]
          air_conditions["pollutants"] = raw_air_conditions["pollutants"]


     for day in forecast_weather["daily"]:

          city_forecast = {
               "forecast_date" : unix_timestamp_converter(day['dt'], date_format="%d/%m/%Y"),
               "weather" : day["weather"],
               "temp" : day["temp"],
               "humidity" : day["humidity"],
               "wind" : day["wind_speed"]}
          
          forecast_info.append(city_forecast)

     for hour in forecast_weather["hourly"][:12]:

          hour_city_forecast = {
               "hour" : unix_timestamp_converter(hour["dt"], date_format="%H:%M"),
               "description" : hour["weather"][0]["description"],
               "icon" : hour["weather"][0]["icon"],
               "temp" : hour["temp"]
               }
          
          hourly_forecast.append(hour_city_forecast)
     

     if "alerts" in forecast_weather:
          alertRegex =  re.compile(r'https://www\.\w+\.\w+(\.\w+)*[^\"]')
          alert = forecast_weather["alerts"][0]["description"]
          alert = alertRegex.sub(make_link, alert)

     return render(request, "city.html", {
          "city" : city,
          "error" : error,
          "city_info" : city_info,
          "map_key" : settings.KEYS['map_key'],
          "date" : formatted_date,
          "forecast_info" : forecast_info,
          "alert" : alert,
          "hourly_forecast" : hourly_forecast,
          "air_conditions" : air_conditions
          })
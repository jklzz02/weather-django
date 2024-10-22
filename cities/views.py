from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import City
from services.utilities import make_link, unix_timestamp_converter, suggest_city
from services.weather import get_weather, get_air_conditions
from typing import Optional, Tuple
import asyncio
import re

def home(request):
    
    async def get_cities_info(cities: list) -> Optional[list]:
        return await asyncio.gather(*(get_weather(city["name"], city["lat"], city["lon"]) for city in cities))

    cities = City.objects.filter(country_code=settings.COUNTRY_CODE).order_by('-population')[:5]

    start_cities = [{"name": city.name, "lat": city.latitude, "lon": city.longitude} for city in cities]
    start_cities_info = asyncio.run(get_cities_info(start_cities))

    return render(request, "home.html", {"start_cities_info": start_cities_info})

def city(request):
     city_info = ""  
     forecast_weather = "" 
     alert = ""
     air_conditions = {}
     forecast_info = [] 
     hourly_forecast = []

     city = request.GET.get("city")

     if city is None or not city.strip():
          referer = request.META.get('HTTP_REFERER')
          return HttpResponseRedirect(referer if referer else reverse("home"))

     formatted_date = datetime.now().strftime('%d/%m/%Y %H:%M')

     city_info = asyncio.run(get_weather(city=city))

     if not city_info:
          suggestions = suggest_city(city)
          return render(request, "city.html", {"city" : city, "suggestions" : suggestions, "error" : True})     

     async def weather_info(lat :str, lon: str) -> Optional[Tuple[dict, dict]]:

          forecast_weather, air_conditions = await asyncio.gather(
                    get_weather(lat=lat, lon=lon, mode="forecast"),
                    get_air_conditions(lat, lon)
               )

          return forecast_weather, air_conditions
          
     forecast_weather, raw_air_conditions = asyncio.run(
          weather_info(
               city_info['coord']['lat'],
               city_info['coord']['lon']
          ))
        
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
          "city_info" : city_info,
          "map_key" : settings.KEYS['map_key'],
          "date" : formatted_date,
          "forecast_info" : forecast_info,
          "alert" : alert,
          "hourly_forecast" : hourly_forecast,
          "air_conditions" : air_conditions
          })

from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from services.utilities import make_link, unix_timestamp_converter, translate
from services.weather import get_current_weather, get_forecast_weather, get_air_conditions
from typing import Optional, Tuple
import asyncio
import re

# weather API
def home(request):
    
    async def get_cities_info() -> Optional[list]:
     start_cities = ["turin", "rome, it", "florence", "naples", "milan"]
     return await asyncio.gather(*(get_current_weather(city) for city in start_cities))
    
    start_cities_info = asyncio.run(get_cities_info())

    return render(request, "home.html", {"start_cities_info" : start_cities_info})

def city(request):
     city_info = ""
     forecast_weather= ""
     air_conditions = {}
     alert = ""
     forecast_info = []
     hourly_forecast = []
     error = False

     city = request.GET.get("city")

     if city is None or not city.strip():
          referer = request.META.get('HTTP_REFERER')
          return HttpResponseRedirect(referer if referer else reverse("home"))

     today = datetime.now()
     formatted_date = translate(today.strftime('%A %d/%m/%Y %H:%M'))

     async def weather_info() -> Optional[Tuple[dict, dict, dict]]:
          city_info = await get_current_weather(city)
          
          if city_info:
               lat = city_info['coord']['lat']
               lon = city_info['coord']['lon']

               forecast_weather, air_conditions = await asyncio.gather(get_forecast_weather(lat, lon), get_air_conditions(lat, lon))

               return city_info, forecast_weather, air_conditions
          
          return None, None, None
          
     city_info, forecast_weather, raw_air_conditions = asyncio.run(weather_info())


     if not city_info:
          error = True

     if not error:

          if not forecast_weather:
               return render(request, "city.html", {"city" : city, "error" : True})

          
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

               forecast_date = translate(unix_timestamp_converter(day['dt'], date_format="%A %d/%m/%Y"))
               summary = translate(day["summary"])
               weather = day["weather"]
               temp = day["temp"]
               humidity = day["humidity"]
               wind = day["wind_speed"]

               city_forecast = {
                    "forecast_date" : forecast_date,
                    "summary" : summary,
                    "weather" : weather,
                    "temp" : temp,
                    "humidity" : humidity,
                    "wind" : wind}
               
               forecast_info.append(city_forecast)

          for i, hour in enumerate(forecast_weather["hourly"]):

               if i >= 12:
                    break

               hour_date = unix_timestamp_converter(hour["dt"], date_format="%H:%M")
               description = hour["weather"][0]["description"]
               icon = hour["weather"][0]["icon"]
               hour_temp = hour["temp"]

               hour_city_forecast = {"hour" : hour_date, "description" : description, "icon" : icon, "temp" : hour_temp }
               hourly_forecast.append(hour_city_forecast)
          

          if "alerts" in forecast_weather:
               alertRegex =  re.compile(r'https://www\.\w+\.\w+(\.\w+)*[^\"]')
               alert = forecast_weather["alerts"][0]["description"]
               alert = translate(alert)
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

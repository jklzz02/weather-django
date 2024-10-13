from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from googletrans import Translator
from services.utilities import make_link, unix_timestamp_converter, translate
from services.weather import get_current_weather, get_forecast_weather, get_air_conditions
import re

# weather API
def home(request):
    start_cities = ["turin", "rome, it", "florence", "naples", "milan"]
    
    start_cities_info = [get_current_weather(city) for city in start_cities]

    return render(request, "home.html", {"start_cities_info" : start_cities_info})

def city(request):
     translator = Translator()
     city_info = ""
     forecast_weather= ""
     air_conditions = {}
     alert = ""
     forecast_info = []
     hourly_forecast = []
     error = False

     city = request.GET.get("city").strip()

     if not city:
          referer = request.META.get('HTTP_REFERER')
          return HttpResponseRedirect(referer if referer else reverse("home"))

     today = datetime.now()
     formatted_date = translate(translator, today.strftime('%A %d/%m/%Y %H:%M'))
     
     city_info = get_current_weather(city)

     if not city_info:
          error = True

     if not error:

          lat = city_info['coord']['lat']
          lon = city_info['coord']['lon']

          forecast_weather = get_forecast_weather(lat, lon)

          if not forecast_weather:
               error = True
               HttpResponseRedirect(reverse("city.html"))

          raw_air_conditions = get_air_conditions(lat, lon)
          
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

               forecast_date = translate(translator, unix_timestamp_converter(day['dt'], date_format="date"))
               summary = translate(translator, day["summary"])
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

               hour_date = unix_timestamp_converter(hour["dt"], date_format="hour")
               description = hour["weather"][0]["description"]
               icon = hour["weather"][0]["icon"]
               hour_temp = hour["temp"]

               hour_city_forecast = {"hour" : hour_date, "description" : description, "icon" : icon, "temp" : hour_temp }
               hourly_forecast.append(hour_city_forecast)
          

          if "alerts" in forecast_weather:
               alertRegex =  re.compile(r'https://www\.\w+\.\w+(\.\w+)*[^\"]')
               alert = forecast_weather["alerts"][0]["description"]
               alert = translate(translator, alert)
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

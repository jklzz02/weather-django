from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from googletrans import Translator
from .services.funcs import make_link, unix_timestamp_converter, translate
from .services.Weather import Weather
import datetime
import re

keys = settings.KEYS
user_info = settings.USER_INFO
lang =  user_info["language"]

# weather API
weather_service = Weather(keys['weather_key'], keys['air_key'])

#regex for urls in alert
alertRegex =  re.compile(r'https://www\.\w+\.\w+(\.\w+)*[^\"]')

# views
def index(request):
    start_cities = ["turin", "rome, it", "florence", "naples", "milan"]
    
    start_cities_info = [weather_service.current(city, lang) for city in start_cities]

    return render(request, "index.html", {"start_cities_info" : start_cities_info})


def city_page(request):
     translator = Translator()
     city_info = ""
     forecast_weather = ""
     air_conditions = {}
     alert = ""
     forecast_info = []
     hourly_forecast = []
     error = False

     city = request.GET.get("city")

     today = datetime.datetime.now()
     formatted_date = translate(translator, today.strftime('%A %d/%m/%Y %H:%M'), lang)
     
     city_info = weather_service.current(city, lang)

     if not city_info:
          error = True

     if not error:

          lat = city_info['coord']['lat']
          lon = city_info['coord']['lon']

          forecast_weather = weather_service.forecast(lat, lon, lang)

          if not forecast_weather:
               error = True
               HttpResponseRedirect(reverse("city.html"))

          raw_air_conditions = weather_service.air_condition(lat, lon, lang)
          
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

               forecast_date = translate(translator, unix_timestamp_converter(day['dt'], date_format="date"), lang)
               summary = translate(translator, day["summary"], lang)
               weather = day["weather"]
               temp = day["temp"]
               humidity = day["humidity"]
               wind = day["wind_speed"]

               city_forecast = {"forecast_date" : forecast_date, "summary" : summary, "weather" : weather, "temp" : temp, "humidity" : humidity, "wind" : wind}
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
               alert = forecast_weather["alerts"][0]["description"]
               alert = translate(translator, alert, lang)
               alert = alertRegex.sub(make_link, alert)


     if not city:
           return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

     return render(request, "city.html", {"city" : city, "error" : error, "city_info" : city_info, "map_key" : keys['map_key'], "date" : formatted_date, "forecast_info" : forecast_info, "alert" : alert, "hourly_forecast" : hourly_forecast, "air_conditions" : air_conditions})

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from dotenv import load_dotenv
from googletrans import Translator
from .services import *
from django.conf import settings
import datetime
import os
import re


load_dotenv()
key = os.getenv("API_KEY")
map_key = os.getenv("MAP_KEY")

# building translator object from library
translator = Translator()

#getting user infos from settings
user_info = settings.USER_INFO

# get user lang from ip
lang =  user_info["language"]

#regex for urls in alert
alertRegex =  re.compile(r'https://www\.\w+\.\w+(\.\w+)*[^\"]')

# views
def index(request):
    city_info = ""
    start_cities = ["torino", "roma, it", "firenze", "napoli", "palermo"]

    if request.session.get("start_cities_info"):
         start_cities_info = request.session.get("start_cities_info")

    else:
        start_cities_info = []

        for city in start_cities:
               start_cities_info.append(get_weather(city, key, lang))
        
    request.session["start_cities_info"] = start_cities_info
    print(get_weather.cache_info())

    return render(request, "index.html", {"city_info" : city_info, "start_cities_info" : start_cities_info})


def city_page(request):
     city = request.GET.get("id")
     city_info = ""
     forecast_weather = ""
     alert = ""
     forecast_info = []
     hourly_forecast = []
     error = False

     today = datetime.datetime.now()
     formatted_date = translate(translator, today.strftime('%A %d/%m/%Y %H:%M'), lang)
     print(today, formatted_date)

     if city:
      city = city.replace("/", "")
     
     if request.method == "POST":

        city = request.POST.get('city')
            
     city_info = get_weather(city, key, lang)

     if city_info["cod"] != 200:
          error = True

     if not error:

          lat = city_info['coord']['lat']
          lon = city_info['coord']['lon']

          forecast_weather = get_forecast_weather(lat, lon, key, lang)
          
          for day in forecast_weather["daily"]:

               forecast_date = translate(translator, unix_converter(day['dt'], date_format="date"), lang)
               summary = translate(translator, day["summary"], lang)
               weather = day["weather"]
               temp = day["temp"]
               humidity = day["humidity"]
               wind = day["wind_speed"]

               city_forecast = {"forecast_date" : forecast_date, "summary" : summary, "weather" : weather, "temp" : temp, "humidity" : humidity, "wind" : wind}
               forecast_info.append(city_forecast)

          for hour in forecast_weather["hourly"]:
 
               hour_date = unix_converter(hour["dt"], date_format="hour")
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
          return HttpResponseRedirect(reverse("index"))


     return render(request, "city.html", {"city" : city, "error" : error, "city_info" : city_info, "map_key" : map_key, "date" : formatted_date, "forecast_info" : forecast_info, "alert" : alert, "hourly_forecast" : hourly_forecast[0:12]})
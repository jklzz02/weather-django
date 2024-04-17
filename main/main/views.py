from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from dotenv import load_dotenv
from functools import lru_cache
from googletrans import Translator
from pprint import pprint
import geocoder
import datetime
import requests
import os


load_dotenv()
key = os.getenv("API_KEY")
map_key = os.getenv("MAP_KEY")

# building translator object from library
translator = Translator()

@lru_cache
def get_country():
     g = geocoder.ip('me')
     return g.country

# get user language form ip with geocoder
lang = get_country()


#get current weather conditions from API
@lru_cache
def get_weather(city, key, lang):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang={lang}'
        weather_data = requests.get(request_url).json()
        pprint(weather_data)
        return weather_data

# get forecast info from API
@lru_cache
def get_forecast_weather(lat, lon, key, lang):
     request_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,current&appid={key}&units=metric&lang={lang}'
     forecast_data = requests.get(request_url).json()
     pprint(forecast_data)
     return(forecast_data)

# timestamp to readable date
def unix_converter(timestamp):
     dt_object = datetime.datetime.fromtimestamp(timestamp)
     readable_date = dt_object.strftime("%d/%m/%Y")
     return readable_date

# treanslate text to italian we could add a paramater to translate from geo infos of user
def translate(translator, text, lang):
     translation = translator.translate(text, dest=lang)
     return translation.text
     

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
     error = False

     today = datetime.datetime.now()
     formatted_date = today.strftime('%d/%m/%Y %H:%M')
     print(today, formatted_date)

     if city:
      city = city.replace("/", "")
     
     if request.method == "POST":

        city = request.POST.get('city')
            
     city_info = get_weather(city, key, lang)

     if city_info["cod"] != 200:
          error = True

     pprint(city_info)    
     print(get_weather.cache_info())

     if not error:

          lat = city_info['coord']['lat']
          lon = city_info['coord']['lon']

          forecast_weather = get_forecast_weather(lat, lon, key, lang)
          
          for day in forecast_weather["daily"]:

               data = unix_converter(day["dt"])
               summary = translate(translator, day["summary"], lang)
               weather = day["weather"]
               temp = day["temp"]
               humidity = day["humidity"]
               wind = day["wind_speed"]

               city_forecast = {"data" : data, "summary" : summary, "weather" : weather, "temp" : temp, "humidity" : humidity, "wind" : wind}
               forecast_info.append(city_forecast)

          if "alerts" in forecast_weather:
               alert = forecast_weather["alerts"][0]["description"]
               alert = translate(translator, alert, lang)

          print("############################################FORECAST INFO#########################################################")
          pprint(forecast_info)

     if not city:
          return HttpResponseRedirect(reverse("index"))


     return render(request, "city.html", {"city" : city, "error" : error, "city_info" : city_info, "map_key" : map_key, "date" : formatted_date, "forecast_info" : forecast_info, "alert" : alert})
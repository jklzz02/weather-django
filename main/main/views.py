from django.http import request
from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
import pprint

load_dotenv()
key = os.getenv("API_KEY")

def get_weather(city, key):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang=it'
        weather_data = requests.get(request_url).json()
        return weather_data

def index(request):
    city_info = ""
    start_cities = ["torino", "roma, it", "firenze", "napoli", "palermo"]

    if request.session.get("start_cities_info"):
         start_cities_info = request.session.get("start_cities_info")
    else:
        start_cities_info = []
        for city in start_cities:
                start_cities_info.append(get_weather(city, key))
        
        request.session["start_cities_info"] = start_cities_info

    pprint.pprint(start_cities_info)     


    return render(request, "index.html", {"city_info" : city_info, "start_cities_info" : start_cities_info})


def city_page(request):
     city = request.GET.get("id")

     if city:
          city = city.replace("/", "")
     city_info = ""
     if request.method == "POST":

        city = request.POST.get('city')
            
     if city:
        city_info = get_weather(city, key)
       


     return render(request, "city.html", {"city" : city, "city_info" : city_info})
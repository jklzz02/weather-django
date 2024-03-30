from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from dotenv import load_dotenv
import requests
import pprint
import os


load_dotenv()
key = os.getenv("API_KEY")
def get_weather(city, key):
        request_url = f'https://api.openweathermap.org/data/2.5/weather?appid={key}&q={city}&units=metric&lang=it'
        weather_data = requests.get(request_url).json()
        print(weather_data)
        return weather_data

def index(request):
    city_info = ""
    start_cities = ["torino", "roma, it", "firenze", "napoli", "palermo"]

    if request.session.get("start_cities_info"):
         start_cities_info = request.session.get("start_cities_info")
         print("non lo sto facendo")
    else:
        start_cities_info = []
        for city in start_cities:
                start_cities_info.append(get_weather(city, key))
                print("lo sto facendo")
        
        request.session["start_cities_info"] = start_cities_info


    return render(request, "index.html", {"city_info" : city_info, "start_cities_info" : start_cities_info})


def city_page(request):
     city = request.GET.get("id")
     city_info = ""
     error = False

     if city:
      city = city.replace("/", "")
     
     if request.method == "POST":

        city = request.POST.get('city')
            
     city_info = get_weather(city, key)

     if city_info["cod"] != 200:
          error = True


     pprint.pprint(city_info)    


     return render(request, "city.html", {"city" : city, "error" : error, "city_info" : city_info})
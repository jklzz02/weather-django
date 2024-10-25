from django.urls import path, re_path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('city/', views.city, name="city"),
    re_path(r'^cities/(?P<page>\d*)$', views.cities_list, name="cities_list"),
]

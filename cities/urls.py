from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('city/', views.city, name="city"),
    path('cities/<int:page>', views.cities_list, name="info")
]

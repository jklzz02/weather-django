from django.urls import path
from . import views

urlpatterns = [
    path('user/login/', views.login, name="login"),
    path('user/register/', views.register, name="register"),
    path('user/profile/', views.profile, name="profile")
]

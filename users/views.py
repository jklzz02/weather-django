from django.shortcuts import render
from django.http import HttpResponse

def register(request):
    return HttpResponse("register")

def login(request):
    return HttpResponse("login")

def profile(request):
    return HttpResponse("user profile")
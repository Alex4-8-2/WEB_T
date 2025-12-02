"""URLs"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from rest_framework.authtoken.views import obtain_auth_token

def home(request):
    return render(request, 'frontend/index.html')

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_auth_token, name='api_login'),
]

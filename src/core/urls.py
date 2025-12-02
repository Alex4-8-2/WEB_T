from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Sistema funcionando</h1><p><a href='/admin/'>Admin Panel</a></p>")

urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
]

"""carga URL configuration"""

#from django.urls import path
from django.conf.urls import url

from carga.views import *


app_name = "carga"
urlpatterns = [
    url(r'^carga', mainCargaArchivos, name='carga'), 
] 

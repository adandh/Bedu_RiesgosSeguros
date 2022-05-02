"""sensibilidad URL configuration"""

#from django.urls import path
from django.conf.urls import url

from sensibilidad.views import *


app_name = "sensibilidad"
urlpatterns = [
    url(r'^activo', mainSensibilidadActivo, name='activo'),
    url(r'^balance', mainSensibilidadBalance, name='balance'),
]
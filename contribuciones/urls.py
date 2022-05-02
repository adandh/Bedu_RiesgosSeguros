"""contribuciones URL configuration"""

#from django.urls import path
from django.conf.urls import url

from contribuciones.views import *


app_name = "contribuciones"
urlpatterns = [
    url(r'^activo', mainActivo, name='activo'),
    url(r'^balance', mainBalance, name='balance'),
] 

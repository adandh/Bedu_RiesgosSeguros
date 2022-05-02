"""salida URL configuration"""

#from django.urls import path
from django.conf.urls import url

from salida.views import *


app_name = "salida"
urlpatterns = [
    url(r'^main', main, name='main'), 
    url(r'^success$', success, name='success'),    
    url(r'^limpiar$', main_limpieza_salida, name='limpiar'),  
]

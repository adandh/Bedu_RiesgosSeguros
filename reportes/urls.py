"""reportes URL configuration"""

#from django.urls import path
from django.conf.urls import url

from reportes.views import *


app_name = "reportes"
urlpatterns = [
    url(r'^reporte1', mainReporte1, name='reporte1'),
    url(r'^reporte2', mainReporte2, name='reporte2'),
    url(r'^reporte3', mainReporte3, name='reporte3'),
    url(r'^reporte4', mainReporte4, name='reporte4'),
    url(r'^reporte5', mainReporte5, name='reporte5'),
]

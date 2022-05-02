"""metricas URL configuration"""

#from django.urls import path
from django.conf.urls import url

from metricas.views import *


app_name = "metricas"
urlpatterns = [
    url(r'^metricasriesgo_validacion/(?P<rcs_id>\d+)/$', validacionInsumos, name='metricasriesgo_validacion'),
    url(r'^metricasriesgo_borrado/(?P<rcs_id>\d+)/$', borradoInsumos, name='metricasriesgo_borrado'),
    url(r'^metricasriesgo', mainMetricasRiesgo, name='metricasriesgo'),
    url(r'^results/(?P<id>\d+)/$', download_zip, name='results'),
]

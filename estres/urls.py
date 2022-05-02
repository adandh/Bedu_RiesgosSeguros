"""estres URL configuration"""

#from django.urls import path
from django.conf.urls import url

from estres.views import *


app_name = "estres"
urlpatterns = [
    url(r'^exploratorio_validacion/(?P<rcs_id>\d+)/$', validacionInsumosExploratorio, name='exploratorio_validacion'),
    url(r'^exploratorio_confirmacion/(?P<rcs_id>\d+)/$', mainConfirmacionExploratorio, name='exploratorio_confirmacion'),
    url(r'^exploratorio_borrado/(?P<rcs_id>\d+)/$', borradoInsumosExploratorio, name='exploratorio_borrado'),
    url(r'^exploratorio', mainExploratorio, name='exploratorio'),
    url(r'^financiero', mainFinanciero, name='financiero'),
    url(r'^vida', mainVida, name='vida'),
    url(r'^noVida', mainNoVida, name='noVida'),
    url(r'^results/(?P<id>\d+)/$', download_zip, name='results'),
]

"""RiesgosSeguros URL Configuration"""

#from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, logout_then_login


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^portal/', include(('portal.urls', 'portal'), namespace='portal')),
    url(r'^metricas/', include(('metricas.urls', 'metricas'), namespace='metricas')),
    url(r'^contribuciones/', include(('contribuciones.urls','contribuciones'), namespace='contribuciones')),   
    url(r'^estres/', include(('estres.urls', 'estres'), namespace='estres')), 
    url(r'^carga/', include(('carga.urls', 'carga'), namespace='carga')),
    url(r'^salida/', include(('salida.urls', 'salida'), namespace='salida')),   
    url(r'^sensibilidad/', include(('sensibilidad.urls', 'sensibilidad'), namespace='sensibilidad')),   
    url(r'^backtesting/', include(('backtesting.urls', 'backtesting'), namespace='backtesting')),   
    url(r'^reportes/', include(('reportes.urls', 'reportes'), namespace='reportes')),   
    url(r'^', LoginView.as_view(template_name='portal/login.html'), name='login'), 
    url(r'^logout/', logout_then_login, name='logout'),  
]

"""portal URL configuration"""

#from django.urls import path
from django.conf.urls import url, include

from portal.views import *


app_name = "portal"
urlpatterns = [
    url(r'^$', index, name='index'),
] 

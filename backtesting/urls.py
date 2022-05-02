"""backtesting URL configuration"""

#from django.urls import path
from django.conf.urls import url

from backtesting.views import *


app_name = "backtesting"
urlpatterns = [
    url(r'^backtesting', mainBacktesting, name='backtesting'),
]

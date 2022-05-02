from __future__ import unicode_literals

from django.contrib import admin
from estres.models import *


# Registro de los modelos definidos en 'models'
admin.site.register(EstresModel)
admin.site.register(ResultadosEstres)

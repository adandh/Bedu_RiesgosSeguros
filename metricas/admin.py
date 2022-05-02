from __future__ import unicode_literals

from django.contrib import admin
from metricas.models import *


# Registro de los modelos definidos en 'models'
admin.site.register(MetricasRiesgoModel)
admin.site.register(ResultadosMetricasRiesgo)

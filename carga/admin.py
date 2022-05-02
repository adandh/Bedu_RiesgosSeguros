from __future__ import unicode_literals

from django.contrib import admin
from carga.models import *


# Registro de los modelos definidos en 'models'
admin.site.register(CargaArchivosModel)
admin.site.register(ResultadosCargaArchivos)

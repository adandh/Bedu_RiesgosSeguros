from __future__ import unicode_literals

import datetime
import shutil
import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings

from carga.models import *


@login_required
def main(request):  
    return render(request, 'salida/main.html')

@login_required
def main_limpieza_salida(request):
    try:
        lista_archivos = os.listdir(settings.MEDIA_ROOT + 'uploads/' + 'user_{0}'.format(request.user) + '/carga_archivos')
    except FileNotFoundError:
        lista_archivos = ['No se encontraron archivos .mat en la carpeta de carga actual']
    return render(request, 'salida/limpiar.html', {'lista_archivos':lista_archivos})
    
@login_required
def success(request):
    path_uploads = settings.MEDIA_ROOT+'uploads/'+'user_{0}'.format(request.user)
    print (path_uploads)
    user =request.user
    rcs_carga = CargaArchivosModel.objects.filter(owner=user)
    rcs_carga.delete()    
    try:
        shutil.rmtree(path_uploads)
    except FileNotFoundError:
        pass
    return render(request, 'salida/success.html')


from __future__ import unicode_literals

import datetime
import shutil
import os
from scipy.io import loadmat, savemat

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate

from carga.models import *
from carga.forms import *



@login_required
def mainCargaArchivos(request):
    print('Estoy en carga:views:mainCargaArchivos')
    user =request.user
    if request.method == 'POST':
        form_rcs = CargaArchivosForm(request.POST, request.FILES)
        if form_rcs.is_valid():
            print('Formulario rcs valido')
            rcs_ca=form_rcs.save(commit=False)
            rcs_ca.owner = user
            # En caso de existir la carpeta de carga en la ruta indicada, se borra 
            path_uploads = settings.MEDIA_ROOT + 'uploads/' + 'user_{0}/'.format(rcs_ca.owner.username) + 'carga_archivos'
            if os.path.exists(path_uploads) and os.path.isdir(path_uploads):
                shutil.rmtree(path_uploads)

            today_date = datetime.date.today().strftime("%m/%d/%Y")
            rcs_ca.folio = str (user.id) + "-" + today_date

            rcs_ca.save()
            lista_archivos = [str(rcs_ca.par).split('/')[-1], str(rcs_ca.lyot).split('/')[-1], str(rcs_ca.lylp).split('/')[-1], str(rcs_ca.sim).split('/')[-1]]

            return render(request, 'carga/success.html',{'lista_archivos':lista_archivos})
        else:
            print('Formulario rcs invalido')
            return render(request, 'carga/mainCargaArchivos.html', {'form':form_rcs})
    else:
        form_rcs = CargaArchivosForm()
        return render(request, 'carga/mainCargaArchivos.html', {'form':form_rcs})


def voidTodict(void):
    ''' Función que recibe como insumo un objeto de tipo void, en este caso,
    utilizamos Layoutglobal y Parametros
    NOTA: Las llave 'Catalogo' y 'Reporte' de Parametros, contienen tablas
    que no son análogas a las de Matlab, por ello se han excluido.'''
    D = {}
    for name in void.dtype.names:
        if name not in ['Catalogo', 'Reporte'] or void.dtype.names[0] != 'General':
            if void[name].dtype.names is None:
                D[name] = void[name]
            else:
                D[name] = voidTodict(void[name][0,0])
    return D
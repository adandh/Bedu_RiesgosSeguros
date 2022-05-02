"""estres views"""

import datetime
import os

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate

from estres.models import *
from estres.forms import *
from estres.tasks import *
from carga.models import CargaArchivosModel

from utils.General.Valida_parametros import Valida_parametros
from utils.General.Valida_RR4LYOT import Valida_RR4LYOT
from utils.A3.Valida_informacionMercado import Valida_informacionMercado



## 1. Modulo Estres Analisis Exploratorio
@login_required
def mainExploratorio(request):    
    print('Estoy en estres:views:mainExploratorio')
    user =request.user
    if request.method == 'POST':
        form_rcs = EstresForm(request.POST, request.FILES)
        if form_rcs.is_valid():
            print('Formulario rcs valido')
            rcs = form_rcs.save(commit=False)
            rcs.owner = user
            today_date = datetime.date.today().strftime("%m/%d/%Y")
            rcs.folio = str (user.id) + "-" + today_date
            rcs_carga = CargaArchivosModel.objects.filter(owner=user).last()
            try:
                rcs.lyot = rcs_carga.lyot
                rcs.par = rcs_carga.par
            except AttributeError:
                return render(request, 'estres/fail_verificacionCarga.html')
            rcs.save()

            # Verificacion de archivos utilizados como insumos
            if str(rcs.par) == '' or str(rcs.lyot) == '':
                return render(request, 'estres/fail_verificacionCarga.html')
            elif str(rcs.info_mercado) == '':
                return render(request, 'estres/fail_verificacionExploratorio.html')
            else:
                lista_archivos = [
                                '"PARAMETROS.mat": '+str(rcs.par).split('/')[-1],
                                '"RR4LYOT.mat": '+str(rcs.lyot).split('/')[-1],
                                '"INFO_MERCADO.xlsx": '+str(rcs.info_mercado).split('/')[-1],
                                ]
                # Creacion de lista de archivos con error de fecha de corte y fecha de corte considerada (devuelta en formato YYYYMMDD)
                lista_errorFecha, fecha_corte = listaErrorFecha(lista_archivos, rcs)
                if len(lista_errorFecha)>0:
                    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
                    borradoEspecificos_Exploratorio(rcs)
                    return render(request, 'estres/fail_fechaExploratorio.html', {'lista_errorFecha':lista_errorFecha, 'fecha_corte':fecha_corte})
                else:
                    return render(request, 'estres/success_verificacionExploratorio.html', {'lista_archivos':lista_archivos, 'rcs_id':rcs.id})

        else:
            print('Formulario rcs invalido')
            print(form_rcs)
            return render(request, 'estres/mainExploratorio.html', {'form':form_rcs})
    else:
        form_rcs = EstresForm()
        return render(request, 'estres/mainExploratorio.html', {'form':form_rcs})


@login_required
def validacionInsumosExploratorio(request,*args,**kwargs):
    fecha_sol = datetime.datetime.now() # Fecha de envio de solicitud 
    print('Estoy en estres:views:validacionInsumosExploratorio')
    rcs_id = kwargs['rcs_id']
    rcs = EstresModel.objects.get(pk=rcs_id)

    insumos_especificos = insumosEspecificos_Exploratorio(rcs) # Construccion de diccionario con insumos especificos utilizados
    analisis_sol= "Estrés - Análisis Exploratorio - Validación" # Nombre para el analisis solicitado
    carpeta_zip = 'estresExploratorio_Validacion_' + 'user_{0}_{1}'.format(rcs.owner.username, rcs.id) # Nombre para carpeta zip
    path_results = settings.RESULTS_ROOT + 'estres_validacion/user_{0}_{1}/'.format(rcs.owner.username, rcs.id) # Ruta para guardar archivos .log de errores
    try:
        os.makedirs(path_results)
    except FileExistsError:
        pass

    # Validacion de insumos (banderas indicadoras y guardado de archivos .log en caso de errores)
    b1 = Valida_parametros(rcs, path_results)
    b2 = Valida_RR4LYOT(rcs, path_results)
    b3 = Valida_informacionMercado(rcs, path_results)

    if b1==1 and b2==1 and b3==1:
        print('Proceso de Validacion exitoso')
        lista_archivos = [
                        '"PARAMETROS.mat": '+str(rcs.par).split('/')[-1],
                        '"RR4LYOT.mat": '+str(rcs.lyot).split('/')[-1],
                        '"INFO_MERCADO.xlsx": '+str(rcs.info_mercado).split('/')[-1],
                        ]
        return render(request, 'estres/success_validacionExploratorio.html',{'rcs_id':rcs.id,'lista_archivos':lista_archivos})
    else:
        # Creacion de carpeta zip de resultados y envio por correo
        result = ResultadosEstres()
        envioCorreoResultadosZip(result, path_results, carpeta_zip, analisis_sol, fecha_sol, insumos_especificos, rcs)
        # Borrado de carpetas de archivos cargados como insumos especificos del analisis
        borradoEspecificos_Exploratorio(rcs)
        # Lista de archivos que presentaron errores en el proceso de validacion        
        lista_archivos = []
        if b1 == 0:
            lista_archivos.append('"PARAMETROS.mat": '+str(rcs.par).split('/')[-1])
        if b2 == 0:
            ar2 = str(rcs.lyot)
            lista_archivos.append('"RR4LYOT.mat": '+str(rcs.lyot).split('/')[-1])        
        if b3 == 0:
            ar3 = str(rcs.info_mercado)
            lista_archivos.append('"INFO_MERCADO.xlsx": '+str(rcs.info_mercado).split('/')[-1])
        print('Se encontraron errores en el proceso de Validacion')
        return render(request, 'estres/fail_validacionExploratorio.html',{'lista_archivos':lista_archivos})


@login_required
def mainConfirmacionExploratorio(request,*args,**kwargs):
    print('Estoy en estres:views:mainConfirmacionExploratorio')
    rcs_id = kwargs['rcs_id']
    print(rcs_id)
    # Llamada a funcion de tasks que ejecuta proceso de calculo (diferida por el efecto del celery que encola las tareas)
    ejecucion_EstresExploratorio.delay(rcs_id)
    return  render(request, 'portal/success.html')


## 2. Modulo Estres Financiero
@login_required
def mainFinanciero(request):
    print('Estoy en estres:views:mainFinanciero')
    return render(request, 'estres/mainFinanciero.html', {})


## 3. Modulo Estres Vida
@login_required
def mainVida(request):
    print('Estoy en estres:views:mainVida')
    return render(request, 'estres/mainVida.html', {})


## 4. Modulo Estres No-Vida
@login_required
def mainNoVida(request):
    print('Estoy en estres:views:mainNoVida')
    return render(request, 'estres/mainNoVida.html', {})


@login_required
def borradoInsumosExploratorio(request,*args,**kwargs):
    print('Estoy en metricas:views:borradoInsumosExploratorio')
    rcs_id = kwargs['rcs_id']
    rcs = EstresModel.objects.get(pk=rcs_id)
    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
    borradoEspecificos_Exploratorio(rcs)
    contexto={} 
    return render(request, 'portal/index.html', contexto)



###############################

def download_zip(request, id):
    print("Estoy en estres:views:download_zip - " + str(id))
    if request.method == 'POST':
        us =  request.POST['username']
        passw =  request.POST['password']
        user = authenticate(username=us, password=passw)
        if user is not None:
            result = ResultadosEstres.objects.get(pk=id)
            zip_path = result.zip_file
            zip_file =  open(zip_path, 'rb')
            response = HttpResponse(zip_file, content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=%s' % str(zip_path).split('/')[-1]
            response['Content-Length'] = os.path.getsize(zip_path)
            zip_file.close()
            return response
        else:
            return render(request, 'portal/login.html')

    else:
        return render(request, 'portal/login.html')

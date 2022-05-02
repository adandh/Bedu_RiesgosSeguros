"""metricas views"""

import datetime
import os
import shutil
from itertools import compress
from numpy import vectorize, where, array

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.core import serializers

from metricas.models import *
from metricas.forms import *
from carga.models import CargaArchivosModel



@login_required
def mainMetricasRiesgo(request):
    print('Estoy en metricas:views:mainMetricasRiesgo')
    user =request.user
    if request.method == 'POST':
        form_rcs = MetricasRiesgoForm(request.POST, request.FILES)
        if form_rcs.is_valid():
            print('Formulario rcs valido')
            rcs = form_rcs.save(commit=False)
            rcs.owner = user
            today_date = datetime.date.today().strftime("%m/%d/%Y")
            rcs.folio = str (user.id) + "-" + today_date
            rcs.fechacorte = ''.join(rcs.fechacorte.split('-'))
            rcs_carga = CargaArchivosModel.objects.filter(owner=user).last()
            rcs.ref = settings.MEDIA_ROOT + 'referencia/' + 'user_{0}/'.format(rcs.owner.username) + 'referencia.mat'
            rcs.catcalif = settings.MEDIA_ROOT + 'calificacionesAgencias/' + 'CatalogoCalificacionesPiP.xlsx'
            dirEntradas = settings.MEDIA_ROOT + 'historicos/' + 'user_{0}/'.format(rcs.owner.username)
            rcs.histocurvas = dirEntradas + 'Historico_CurvasTasas.csv'
            rcs.histospread = dirEntradas + 'Historico_SpreadYield.csv'
            rcs.histoTC = dirEntradas + 'Historico_TiposCambio.csv'
            rcs.histocurvasReportes = dirEntradas + 'Historico_CurvasReportes.csv'


            # Gestion de carpetas de historicos
            rcs.ruta_Layout = dirEntradas + 'Layoutglobal/' # Ruta para objetos .pickle de la cartera (Layoutglobal)
            rcs.ruta_DeuCamb = dirEntradas + 'Param_Deu_Cam_Cap/' # Ruta para objetos .pickle de parametros especificos (deuda, cambiario y capitales)
            rcs.ruta_VectorPrecios = dirEntradas + 'VectorPrecios/' # Ruta para objetos .pickle de informacion relevante del vector de precios
            rcs.ruta_Parametros = dirEntradas + 'Parametros_Referencia/'
            try:
                os.makedirs(rcs.ruta_Layout)
            except FileExistsError:
                pass
            try:
                os.makedirs(rcs.ruta_DeuCamb)
            except FileExistsError:
                pass
            try:
                os.makedirs(rcs.ruta_VectorPrecios)
            except FileExistsError:
                pass

            # Verificacion de que se elige al menos un horizonte de riesgo para procesamiento
            horizonte_lista = ["diario", "semanal", "mensual", "anual"]
            idx = [rcs.horizonte_Diario, rcs.horizonte_Semanal, rcs.horizonte_Mensual, rcs.horizonte_Anual]
            horizonte_lista = list(compress(horizonte_lista, idx)) # Lista de nombres (cadenas texto) de horizontes efectivamente a procesar
            if len(horizonte_lista)==0:
                return render(request, 'metricas/fail_verificacionHorizonte.html', {'val_reaseguro':rcs.val_reaseguro})

            # Verificacion de archivos de carga .mat minimos requeridos
            try:
                rcs.par = rcs_carga.par
                if rcs.val_reaseguro:
                    rcs.lyot = rcs_carga.lyot
            except AttributeError:
                return render(request, 'metricas/fail_verificacionInsumosCarga.html', {'val_reaseguro':rcs.val_reaseguro})
            rcs.save()
            print(rcs.id)

            # Verificacion de archivos utilizados como insumos
            if str(rcs.par) == '' or (str(rcs.lyot) == '' and rcs.val_reaseguro):
                return render(request, 'metricas/fail_verificacionInsumosCarga.html', {'val_reaseguro':rcs.val_reaseguro})
            elif str(rcs.rr7port) == '' or str(rcs.vecpip) == '' or str(rcs.curpip) == '':
                # Borrado de carpetas de archivos cargados como insumos especificos del analisis
                borradoEspecificos(rcs)
                return render(request, 'metricas/fail_verificacionInsumosMetricas.html')
            else:
                lista_archivos = ['"PARAMETROS.mat": ' + str(rcs.par).split('/')[-1]]
                if (str(rcs.lyot)!='' and rcs.val_reaseguro):
                    lista_archivos.append('"RR4LYOT.mat": ' + str(rcs.lyot).split('/')[-1])
                lista_archivos = lista_archivos + ['"RR7PORTAFOLIOS.xlsx": ' + str(rcs.rr7port).split('/')[-1],
                                                    '"VECTORPIP.xls": ' + str(rcs.vecpip).split('/')[-1],
                                                    '"CURVASPIP.xls": ' + str(rcs.curpip).split('/')[-1],
                                                    ]
                if str(rcs.rr7inmu)!='':
                    lista_archivos.append('"RR7EFITRINMU.txt": ' + str(rcs.rr7inmu).split('/')[-1])
                if str(rcs.rr4imprec)!='':
                    lista_archivos.append('"RR4IMPREC.txt": ' + str(rcs.rr4imprec).split('/')[-1])
                if str(rcs.vec)!='':
                    lista_archivos.append('"VEC.mat": ' + str(rcs.vec).split('/')[-1])
                if str(rcs.cat)!='':
                    lista_archivos.append('"CAT.mat": ' + str(rcs.cat).split('/')[-1])
                # Creacion de lista de archivos con error de fecha de corte y fecha de corte considerada (devuelta en formato YYYYMMDD)
                print(lista_archivos)
                lista_errorFecha, fecha_corte = listaErrorFecha(lista_archivos[(1 + (str(rcs.lyot)!='' and rcs.val_reaseguro)):], rcs)
                if len(lista_errorFecha)>0:
                    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
                    borradoEspecificos(rcs)
                    return render(request, 'metricas/fail_fecha.html', {'lista_errorFecha':lista_errorFecha, 'fecha_corte':fecha_corte})
                else:
                    if str(rcs.rr4imprec) != '' and str(rcs.cat) == '':
                        lista_archivos.append('IMPORTANTE: Dado que se esta proporcionando ' + '"RR4IMPREC.txt": ' + str(rcs.rr4imprec).split('/')[-1] +  ', es necesario incluir el archivo "CAT.mat" correspondiente para que "RR4IMPREC.txt" sea considerado en el análisis.')
                    return render(request, 'metricas/success_verificacionInsumos.html', {'lista_archivos':lista_archivos, 'rcs_id':rcs.id})

        else:
            print('Formulario rcs invalido')
            print(form_rcs)
            return render(request, 'metricas/mainMetricasRiesgo.html', {'form':form_rcs})
    else:
        form_rcs = MetricasRiesgoForm()
        return render(request, 'metricas/mainMetricasRiesgo.html', {'form':form_rcs})

@login_required
def validacionInsumos(request,*args,**kwargs):
    fecha_sol = datetime.datetime.now() # Fecha de envio de solicitud 
    print('Estoy en metricas:views:validacionInsumos')
    rcs_id = kwargs['rcs_id']
    rcs = MetricasRiesgoModel.objects.get(pk=rcs_id)

    insumos_especificos = insumosEspecificos(rcs) # Construccion de diccionario con insumos especificos utilizados
    analisis_sol= "Métricas Riesgo Estándar - Validación" # Nombre para el analisis solicitado
    carpeta_zip = 'metricasRiesgo_Validacion_' + 'user_{0}_{1}'.format(rcs.owner.username, rcs.id) # Nombre para carpeta zip
    path_results = settings.RESULTS_ROOT + 'metricas_validacion/user_{0}_{1}/'.format(rcs.owner.username, rcs.id) # Ruta para guardar archivos .log de errores
    try:
        os.makedirs(path_results)
    except FileExistsError:
        pass

    # Validacion de insumos (banderas indicadoras y guardado de archivos .log en caso de errores)    
    b1 = 1  #Valida_parametros(rcs, path_results)
    b2 = 1
    if rcs.val_reaseguro:
        b2 = 1  #Valida_RR4LYOT_MetricasRiesgoEstandar(rcs, path_results)
    if b1 == 1: # Se requiere insumo 'PARAMETROS.mat' correcto para validar los archivos especificos 
        b3,b4,b5,b6,b7 = 1, 1, 1, 1, 1  #Valida_Archivos_MetricasRiesgoEstandar(rcs, path_results) # Proceso de validacion de archivos especificos
    else:
        b3,b4,b5,b6,b7 = -1,-1,-1,-1,-1

    if b1==1 and b2==1 and b3==1 and b4==1 and b5==1:
        print('Proceso de Validacion exitoso')
        lista_archivos = ['"PARAMETROS.mat": ' + str(rcs.par).split('/')[-1]]
        if rcs.val_reaseguro:
            lista_archivos.append('"RR4LYOT.mat": ' + str(rcs.lyot).split('/')[-1])
        lista_archivos = lista_archivos + ['"RR7PORTAFOLIOS.xlsx": ' + str(rcs.rr7port).split('/')[-1],
                                            '"VECTORPIP.xls": ' + str(rcs.vecpip).split('/')[-1],
                                            '"CURVASPIP.xls": ' + str(rcs.curpip).split('/')[-1],
                                            ]
        # Guardado de parametros referencia .mat (rcs.par) en la carpeta de historicos correspondiente (rcs.ruta_Parametros)
        archivo_origen = rcs.par.path
        archivo_destino = os.path.join(rcs.ruta_Parametros, os.path.basename(rcs.par.path))
        shutil.copyfile(archivo_origen, archivo_destino) # Reemplaza en caso de archivo existente

        if b6 == 1:
            lista_archivos.append('"RR7EFITRINMU.txt": ' + str(rcs.rr7inmu).split('/')[-1])
        if b7 == 1:
            lista_archivos.append('"RR4IMPREC.txt": ' + str(rcs.rr4imprec).split('/')[-1])

        #path_results = settings.RESULTS_ROOT + 'metricas/user_{0}_{1}/'.format(rcs.owner.username, rcs_id) # Ruta para guardar archivos .log de errores
        
        return render(request, 'metricas/success_validacion.html',{'rcs_id':rcs.id,'lista_archivos':lista_archivos})
    else:
        # Creacion de carpeta zip de resultados y envio por correo
        result = ResultadosMetricasRiesgo()
        envioCorreoResultadosZip(result, path_results, carpeta_zip, analisis_sol, fecha_sol, insumos_especificos, rcs)
        # Borrado de carpetas de archivos cargados como insumos especificos del analisis
        borradoEspecificos(rcs)
        # Lista de archivos que presentaron errores en el proceso de validacion
        lista_archivos = []
        if b1 == 0:
            lista_archivos.append('"PARAMETROS.mat": '+str(rcs.par).split('/')[-1])
        if b2 == 0:
            lista_archivos.append('"RR4LYOT.mat": '+str(rcs.lyot).split('/')[-1])
        if b1 == 0:
            lista_archivos.append('IMPORTANTE: El resto de archivos proporcionados NO fueron considerados en el proceso de validación. Serán incluidos una vez que el insumo "PARAMETROS.mat" no presente inconsistencias.')
        if b3 == 0:
            lista_archivos.append('"RR7PORTAFOLIOS.xlsx": '+str(rcs.rr7port).split('/')[-1])
        if b4 == 0:
            lista_archivos.append('"VECTORPIP.xls": '+str(rcs.vecpip).split('/')[-1])
        if b5 == 0:
            lista_archivos.append('"CURVASPIP.xls": '+str(rcs.curpip).split('/')[-1])
        if b6 == 0:
            lista_archivos.append('"RR7EFITRINMU.txt": '+str(rcs.rr7inmu).split('/')[-1])
        if b7 == 0:
            lista_archivos.append('"RR4IMPREC.txt": '+str(rcs.rr4imprec).split('/')[-1])
        print('Se encontraron errores en el proceso de Validacion')
        return render(request, 'metricas/fail_validacion.html',{'lista_archivos':lista_archivos})


@login_required
def borradoInsumos(request,*args,**kwargs):
    print('Estoy en metricas:views:borradoInsumos')
    rcs_id = kwargs['rcs_id']
    rcs = MetricasRiesgoModel.objects.get(pk=rcs_id)
    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
    borradoEspecificos(rcs)
    contexto={}
    return render(request, 'portal/index.html', contexto)


###############################

def download_zip(request, id):
    # Funcion llamada via la url 'rcs_contributions:results' para descarga de la carpeta zip de resultados (uso de parametro 'id' de resultados)
    print("Estoy en metricas:views:download_zip - " + str (id))
    if request.method == 'POST':
        us =  request.POST['username']
        passw =  request.POST['password']
        user = authenticate(username=us, password=passw)
        if user is not None:
            result = ResultadosMetricasRiesgo.objects.get(pk=id)
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


def listaErrorFecha(lista_archivos, rcs):
    # Creacion de lista de archivos con error de fecha de corte y fecha de corte considerada (devuelta en formato YYYYMMDD)
    fecha_corte = ''.join(rcs.fechacorte.split('-')) # Fecha de corte como cadena YYYYMMDD (rcs.fechacorte que mantiene formato YYYY-MM-DD)
    validaFecha = where(~vectorize(lambda t: t.split('.')[-2].endswith(fecha_corte))(lista_archivos))[0] # Indicadoras de archivos con terminacion (penultima posicion bajo 'split') distinta a rcs.fechacorte
    lista_errorFecha = array(lista_archivos)[validaFecha] # Lista de archivos que resultan distintos a fecha.corte
    return (lista_errorFecha, fecha_corte)


def insumosEspecificos(rcs):
    # Construccion de diccionario con insumos especificos proporcionados al modulo para su posterior envio por correo
    lista_archivos_especificos = [str(rcs.rr7port).split('/')[-1]] + [str(rcs.vecpip).split('/')[-1]]+ [str(rcs.curpip).split('/')[-1]] + [str(rcs.rr7inmu).split('/')[-1]] + [str(rcs.rr4imprec).split('/')[-1]] + [str(rcs.vec).split('/')[-1]] + [str(rcs.cat).split('/')[-1]]
    lista_etiquetas = ['Archivo RR7Portafolios.xlsx', 'Archivo vectorPiP.xls', 'Archivo curvasPiP.xls', 'Archivo RR7EFITRINMU.txt', 'Archivo RR4IMPREC.txt', 'Archivo vectorPiP.mat', 'Archivo cat_reaseguro.mat']
    diccionario_archivos = dict(zip(lista_etiquetas, lista_archivos_especificos))
    horizonte_lista = ["diario", "semanal", "mensual", "anual"]
    idx = [rcs.horizonte_Diario, rcs.horizonte_Semanal, rcs.horizonte_Mensual, rcs.horizonte_Anual]
    horizonte_lista = list(compress(horizonte_lista, idx)) # Lista de nombres (cadenas texto) de horizontes efectivamente a procesar
    insumos_especificos = {'Fecha de corte':rcs.fechacorte,
                            'Número de escenarios':rcs.numero_escenarios,
                            'Horizonte de riesgo':horizonte_lista,
                            'Nivel de confianza':rcs.q,
                            }
    insumos_especificos.update(diccionario_archivos)
    return insumos_especificos



def borradoEspecificos(rcs):
    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
    try:
        shutil.rmtree(os.path.dirname(rcs.rr7port.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a RR7Portafolios.xlsx de la compañía.')
    try:
        shutil.rmtree(os.path.dirname(rcs.vecpip.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a VECTORPIP.xls de la compañía.')
    try:
        shutil.rmtree(os.path.dirname(rcs.curpip.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a CURVASPIP.xls de la compañía.')
    try:
        shutil.rmtree(os.path.dirname(rcs.rr7inmu.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a INMUEBLES de la compañía.')
    try:
        shutil.rmtree(os.path.dirname(rcs.rr4imprec.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a IMPORTES RECUPERABLES DE REASEGURO de la compañía.')
    try:
        shutil.rmtree(os.path.dirname(rcs.vec.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a VECTOR PIP.MAT de CNSF.')
    try:
        shutil.rmtree(os.path.dirname(rcs.cat.path),ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a CATALOGO REASEGURADORAS.MAT de CNSF.')

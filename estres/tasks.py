"""estres tasks"""

import datetime
import os
import shutil
from numpy import vectorize, where, array

from celery.decorators import task
from django.conf import settings

from RiesgosSeguros.utils import *
from estres.middleware import *
from estres.models import *


# Se definen funciones para tareas de calculos que se mandan a llamar diferidas en 'views' (diferidas por el efecto del celery que encola las tareas)
# Las funciones exe_xxxx() llaman a funciones de calculos definidas en 'middleware' y generan carpetas zip de resultados que son enviadas al usuario via correo
# Se incluyen funciones complementarias que permiten el envio por correo y generan listas de insumos especificos y archivos con error de fecha de corte

@task(name="ejecucion_EstresExploratorio")
def ejecucion_EstresExploratorio(rcs_id):
    fecha_sol = datetime.datetime.now() # Fecha de envio de solicitud 
    print('Estoy en estres:tasks:exe_estress_ae')
    rcs = EstresModel.objects.get(pk=rcs_id)
    
    insumos_especificos = insumosEspecificos_Exploratorio(rcs) # Construccion de diccionario con insumos especificos utilizados
    analisis_sol= "Estrés - Análisis Exploratorio" # Nombre para el analisis solicitado
    carpeta_zip = 'estresExploratorio_' + 'user_{0}_{1}'.format(rcs.owner.username, rcs_id) # Nombre para carpeta zip
    path_results = settings.RESULTS_ROOT + 'estres/user_{0}_{1}/'.format(rcs.owner.username, rcs_id) # Ruta para guardar archivos .log de errores
    try:
        os.makedirs(path_results)
    except FileExistsError:
        pass
    # Correo de notificacion de envio de peticion del analisis solicitado
    send_mail_notificacion(rcs.owner.email, analisis_sol, fecha_sol, insumos_especificos, rcs)
    # Llamada a funcion de middleware que encapsula al script principal de ejecucion de calculos
    calculos_A3_Exploratorio(rcs, path_results)      
    # Creacion de carpeta zip de resultados y envio por correo
    result = ResultadosEstres()
    envioCorreoResultadosZip(result, path_results, carpeta_zip, analisis_sol, fecha_sol, insumos_especificos, rcs)
    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
    borradoEspecificos_Exploratorio(rcs)



###############################

def envioCorreoResultadosZip(result, path_results, carpeta_zip, analisis_sol, fecha_sol, insumos_especificos, rcs):
    # Creacion de carpeta zip de resultados y envio por correo para su descarga
    result.folio = str(rcs.id) + "-" + datetime.date.today().strftime("%m/%d/%Y")
    result.path = path_results
    result.zip_file = zip_out(carpeta_zip, result.path)
    result.save()
    url_results = "estres/results/{0}/".format(result.id) # IMPORTANTE: ruta consistente con la url 'estres:results'
    send_mail(rcs.owner.email, url_results, carpeta_zip, analisis_sol, fecha_sol, insumos_especificos, rcs)


def listaErrorFecha(lista_archivos, rcs):
    # Creacion de lista de archivos con error de fecha de corte y fecha de corte considerada (devuelta en formato YYYYMMDD)
    fecha_corte = ''.join(rcs.fechacorte.split('-')) # Fecha de corte como cadena YYYYMMDD (rcs.fechacorte que mantiene formato YYYY-MM-DD)
    validaFecha = where(~vectorize(lambda t: t.split('.')[-2].endswith(fecha_corte))(lista_archivos))[0] # Indicadoras de archivos con terminacion (penultima posicion bajo 'split') distinta a rcs.fechacorte
    lista_errorFecha = array(lista_archivos)[validaFecha] # Lista de archivos que resultan distintos a fecha.corte
    return (lista_errorFecha, fecha_corte)


def insumosEspecificos_Exploratorio(rcs):
    # Construccion de diccionario con insumos especificos proporcionados al modulo para su posterior envio por correo
    lista_archivos_especificos = [str(rcs.info_mercado).split('/')[-1]]
    lista_etiquetas = ['Archivo INFO_MERCADO.xlsx']
    diccionario_archivos = dict(zip(lista_etiquetas, lista_archivos_especificos))
    horizonte = "anual"
    if round(rcs.horizonte_riesgo*12) == 1:
        horizonte = "mensual"
    elif round(rcs.horizonte_riesgo*52) == 1:
        horizonte = "semanal"
    elif round(rcs.horizonte_riesgo*252) == 1:
        horizonte = "diario"
    insumos_especificos = { 'Fecha de corte':rcs.fechacorte,
                            'Número de escenarios':rcs.numero_escenarios,
                            'Horizonte de riesgo':horizonte,
                            }
    insumos_especificos.update(diccionario_archivos)
    return insumos_especificos

def borradoEspecificos_Exploratorio(rcs):
    # Borrado de carpetas de archivos cargados como insumos especificos del analisis
    try:
        path_uploads = os.path.dirname(rcs.info_mercado.path)
        shutil.rmtree(path_uploads,ignore_errors=True)
    except ValueError:
        print('NO se seleccionó información asociada a INFO_MERCADO.xlsx de la compañía.')



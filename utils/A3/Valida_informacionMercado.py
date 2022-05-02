import pandas as pd
import numpy as np
from datetime import datetime
import os
import logging

from utils.General.set_logger import set_logger


def Valida_informacionMercado(rcs, dirErrores):
    """
    Función que valida el excel consolidadoInfoErrores.xlsx
    :param rcs: Diccionario principal que almacena el archivo de excel en la llave rcs.info_mercado
    :param dirErrores: Ruta de salida donde se guarda el .log con los posibles errores
    :return:
    """
    ''' Variable que monitorea la existencia (o no) de errores'''
    errores = 0

    '''0. Archivo log donde se guardarán los posibles errores.'''
    Nombre = 'consolidadoInfoMercado'
    namelog = dirErrores + Nombre + '.log'  # Creación de archivo con errores en caso de existir errores.
    if os.path.isfile(namelog):
        os.remove(namelog)

    '''Creando archivo .log, asignando nivel ERROR y formato'''
    File = set_logger(Nombre, namelog, level=logging.ERROR)

    '''Lectura del excel'''
    conInfM = pd.read_excel(rcs.info_mercado, keep_default_na=True)

    # '''Nombre de cada columna'''
    # Nombres = ['Fecha',
    # 'BONOSM3M', 'BONOSM6M', 'BONOSM1Y', 'BONOSM2Y', 'BONOSM3Y', 'BONOSM4Y', 'BONOSM5Y', 'BONOSM6Y', 'BONOSM7Y', 'BONOSM8Y', 'BONOSM9Y', 'BONOSM10Y', 'BONOSM15Y', 'BONOSM20Y', 'BONOSM30Y',
    # 'UMS3M', 'UMS6M', 'UMS1Y', 'UMS2Y', 'UMS3Y', 'UMS4Y', 'UMS5Y', 'UMS6Y', 'UMS7Y', 'UMS8Y', 'UMS9Y', 'UMS10Y', 'UMS15Y', 'UMS20Y', 'UMS30Y',
    # 'UDIBONOS3M', 'UDIBONOS6M', 'UDIBONOS1Y', 'UDIBONOS2Y', 'UDIBONOS3Y', 'UDIBONOS4Y', 'UDIBONOS5Y', 'UDIBONOS6Y', 'UDIBONOS7Y', 'UDIBONOS8Y', 'UDIBONOS9Y', 'UDIBONOS10Y', 'UDIBONOS15Y', 'UDIBONOS20Y', 'UDIBONOS30Y',
    # 'TBILLS3M', 'TBILLS6M', 'TBILLS1Y', 'TBILLS2Y', 'TBILLS3Y', 'TBILLS4Y', 'TBILLS5Y', 'TBILLS6Y', 'TBILLS7Y', 'TBILLS8Y', 'TBILLS9Y', 'TBILLS10Y', 'TBILLS15Y', 'TBILLS20Y', 'TBILLS30Y',
    # 'USD', 'UDI', 'IPCCONSUMO', 'IPCMATERIALES', 'IPCINDUSTRIAL', 'IPCFINANCIERO', 'IPCTELECOM', 'IPCCONSUMONF', 'IPC FIBRAS', 'IBONOSMEX', 'VIVIENDASHF', 'SPGLOBAL1200']
    # i = 0
    # for nombre in list(conInfM.columns):
    #     if nombre != Nombres[i]:
    #         errores += 1
    #         File.error('Nombre incorrecto en columna número ' + str(i + 1) + ' (' + \
    #                       'Esperado [' + Nombres[i] + '], Recibido [' + nombre + ']).')
    #     i += 1

    try:
        '''Validación de columna Fecha'''
        Fecs = np.array([t.days for t in conInfM.iloc[:,0].diff()[1:]]) # Primera columna debe contener fechas
        Error = np.where(Fecs <= 0)[0] # Las fechas deben estar en estricto orden ascendente
        if len(Error) > 0:
            R = ''.join(str(e + 2) + ', ' for e in Error[:-1]) if len(Error) > 1 else str(Error[0] + 2)
            R = R[:-2] + ' y ' + str(Error[-1] + 2) if len(Error) > 1 else R
            File.error("Para la columna 'Fecha', los renglones " + R + ' no se encuentran en orden ascendente ' +\
             'con respecto al renglón anterior.')
            errores += 1
        
        '''Validación de que ultimo dato de columna fecha es igual a la fecha de corte'''
        if np.datetime64(rcs.fechacorte).astype(datetime) != conInfM.iloc[-1,0].date():
            File.error("El último valor en la columna 'Fecha' es distinto a la fecha de corte. Favor de verificar que ambos valores sean iguales en los insumos proporcionados.")
            errores += 1

    except (TypeError, AttributeError):
        File.error('La primera columna debe contener datos de tipo fecha. Favor de incluir el formato requerido para series de tiempo.')
        errores += 1


    '''Validación de flotantes (los NA del excel se han convertido a nan)'''
    Cols_num = list(conInfM.columns)[1:]
    Noflt_r, Noflt_c = np.where(~np.vectorize(lambda t: isinstance(t, (float,int)))(conInfM[Cols_num]))
    if len(Noflt_r) > 0:
        c_un, _, ic = np.unique(Noflt_c, axis=0, return_index=True, return_inverse=True)
        for i in range(len(c_un)):
            r = Noflt_r[np.where(ic == i)[0]]
            R = ''.join(str(r[j] + 1) + ', ' for j in range(len(r) - 1)) if len(r) > 1 else str(
                r[0] + 1)
            R = R[:-2] + ' y ' + str(r[-1] + 1) if len(r) > 1 else R
            File.error('La columna ' + str(c_un[i] + 2) + " con nombre '" + Cols_num[c_un[i]] + \
                       "', presenta un tipo de dato distinto de flotante o entero en los renglones: " + \
                        R + ". Si este es un NA, favor de reemplazarlo por 'NA'.")
        errores += 1

    '''Eliminando archivo log (File) del administrador'''
    logging.getLogger().removeHandler(File)
    logging.shutdown()

    '''Eliminando .log si está vacío'''
    if os.stat(namelog).st_size == 0:
        os.remove(namelog)

    bandera = 1 if errores == 0 else 0

    return bandera

from numpy import float64, vectorize, str_, int_, where, uint8, array
from scipy.io import loadmat
from copy import deepcopy
from datetime import datetime
import os.path
import logging

from utils.General.set_logger import set_logger


def Valida_parametros(rcs, dirErrores):
    """Función que se encarga de la validación general del insumo:
    parametros_referencia_yyyymmdd.mat"""

    ''' Variable que monitorea la existencia (o no) de errores'''
    errores = 0

    '''0. Archivo log donde se guardarán los posibles errores.'''
    Nombre = 'parametros' + rcs.fechacorte
    namelog = dirErrores + Nombre + '.log'  # Creación de archivo con errores en caso de existir errores.
    if os.path.isfile(namelog):
        os.remove(namelog)

    '''Creando archivo .log, asignando nivel ERROR y formato'''
    File = set_logger(Nombre, namelog, level=logging.WARN)

    try:
        '''Carga del archivo de parámetros de referencia'''
        param = voidTodict(loadmat(rcs.par)['Parametros'][0,0])
        Actuarial_aux = loadmat(rcs.par)['Parametros']
        if 'Actuarial' in Actuarial_aux.dtype.names:
            Actuarial_aux = Actuarial_aux[0,0]['Actuarial']
            for name in Actuarial_aux.dtype.names: # Ajuste al ramo 'Actuarial'
                for subname in Actuarial_aux[name][0,0].dtype.names:
                    if subname == 'Ramo':
                        forma = Actuarial_aux[name][0, 0][subname][0,0].shape[1]
                        param['Actuarial'][name][subname] =array([[0]*forma], dtype = object)
                        for j in range(param['Actuarial'][name][subname].shape[1]):
                            param['Actuarial'][name][subname][0,j] = Actuarial_aux[name][0,0][subname][0,0][0,j][0]
                    else:
                        param['Actuarial'][name][subname] = deepcopy(Actuarial_aux[name][0,0][subname])
        del Actuarial_aux

        '''Validación de nombres de campos principales'''
        llaves = {'Cambiario':{'sigma':[], 'mu':[], 'tipo':[]},
                  'Deuda':{'alpha':[], 'beta':[], 'sigma':[], 'e0':[], 'spread':[], 'yield':[]},
                  'Spread':{'kappa':[]},
                  'fechacorte':[],
                  'Acciones':{'BMV':[]},'Actuarial':{'FactFianzRecl':[], 'FactFianzGar':[], 'MASMercado': {'Ramo':[]}},
                  'proveedor':[]}

        S1, S2 = set(llaves), set(param)

        if len(S1-S2) > 0:
            for campo_faltante in list(S1-S2):
                if campo_faltante in ['proveedor', 'fechacorte', 'Actuarial', 'Acciones', 'catRR4', 'Pensiones']:
                    File.warning('El campo "' + campo_faltante + '" no se encuentra en el archivo de parámetros de referencia.'\
                                    + ' No es indispensable incluirlo.')
                else:
                    File.error('El campo "' + campo_faltante + '" no se encuentra en el archivo de parámetros de referencia.'\
                                  + ' Debe incluirse para proseguir con la validación de este insumo.')
                    errores += 1

        if len(S2-S1) > 0:
            for campo_no_reconocido in list(S2-S1):
                if campo_no_reconocido not in ['catRR4', 'Pensiones']:  # El campo 'catRR4' será incluido en validaciones posteriores
                    File.warning('"' + campo_no_reconocido + '" no es un campo válido en el archivo de parámetros de referencia.'\
                                  + ' Favor de verificarlo y cargar nuevamente el archivo.')
                    #errores += 1

        '''Validación de subcampos'''
        campos_validos = S1.intersection(S2)
        n_mercados = {} # Número de mercados
        for campo in campos_validos:
            if campo not in ['fechacorte', 'proveedor']:
                error, subcampos = Campos(llaves, param, campo)
            else:
                error, subcampos = [], ['NA']
            for e in error: # Añadiendo errores si es que existen
                File.error(e)
                errores += 1
            if campo == 'Cambiario' and len(subcampos) > 0:
                shape_cambiario = param[campo][subcampos[0]].shape
                #n_mercados[campo] = shape_cambiario[1]
                Nombres = ''.join(subcampos[i] + ', ' for i in range(len(subcampos)-1))[:-2] + ' y ' + subcampos[-1]
                for s in subcampos:
                    if param[campo][s].shape != shape_cambiario:
                        File.error('Hay inconsistencias en el número de mercados de los subcampos: ' + Nombres +\
                                      '; pertenecientes a la rama ' + campo)
                        errores += 1
                    try:
                        param[campo][s].astype(float64)
                    except ValueError:
                        File.error('El tipo de dato del subcampo "' + s + '" de la rama "' + campo + '" no es de tipo flotante. ' + \
                                      'Favor de verificarlo.')
                        errores += 1
            elif campo == 'Deuda' and len(subcampos) > 0:
                n_mercados[campo] = 0
                shape_deuda, error_shape = [], 0 # Número de mercados y variable de error
                n_params = {'alpha':[], 'beta':[], 'sigma':[], 'e0':[], 'error':[]} # Dimensión de cada parámetro por mercado
                Nombres = 'alpha, beta, sigma y/o e0'
                for s in subcampos:
                    shape_deuda.append(param[campo][s].shape)
                    n_mercados[campo] = shape_deuda[0][1] if n_mercados[campo] == 0 else n_mercados[campo]
                    if not all(x == shape_deuda[0] for x in shape_deuda) and error_shape == 0:
                        File.error('Existen inconsistencias en el número de mercados de los subcampos ' + Nombres + \
                                      ' del ramo "' + campo + '". Favor de verificarlo.')
                        error_shape = 1
                        errores += 1
                    if s in ['alpha', 'beta', 'sigma', 'e0']:
                        for j in range(param[campo][s].shape[1]):
                            n_params[s].append(param[campo][s][0,j].shape)
                            try:
                                param[campo][s][0,j].astype(float64)
                            except ValueError:
                                File.error('El tipo de dato del vector (' + str(j+1) + ') del subcampo "' + s +\
                                              '" de la rama "' + campo + '" no es de tipo flotante, favor de verificarlo.')
                                errores += 1
                        if not all(x == n_params[s][0] for x in n_params[s]):
                            n_params['error'].append(s) # Agregando variable con inconsistencias en las dimensiones
                            File.error('Las dimensiones de los vectores de parámetros del subcampo "' + s + '" del ramo "'+\
                                          campo + '", presentan inconsistencias entre ellos. Favor de verificarlo.')
                            errores += 1
                    else: # spread, yield
                        for mercado in range(param[campo][s].shape[1]):
                            for struc in range(param[campo][s][0,mercado].shape[0]):
                                var_struc = param[campo][s][0,mercado][struc,0].dtype.names
                                if 'breaks' not in var_struc or 'coefs' not in var_struc:
                                    File.error('La estructura (' + str(struc+1) + ') del mercado (' + str(mercado+1) +\
                                                  ') en el subcampo "' + s + '" perteneciente al ramo "' + campo + '", ' +\
                                                  'no contiene las variables "breaks" y/o "coefs". Favor de verificarlo y volver a intentar.')
                                    errores += 1
                                else:
                                    try:
                                        param[campo][s][0, mercado][struc, 0]['breaks'][0, 0].astype(float64)
                                        param[campo][s][0, mercado][struc, 0]['coefs'][0, 0].astype(float64)
                                    except ValueError:
                                        File.error('El tipo de dato reportado en la variable "breaks" y/o "coefs" para la '+\
                                                      'estructura (' + str(struc+1) + ') del mercado (' + str(mercado+1) +\
                                                      ') en el subcampo "' + s + '" perteneciente al ramo "' + campo + '", no es de tipo '+\
                                                      'flotante. Favor de verificarlo y volver a intentar.')
                                        errores += 1
                '''Se valida que, para aquellas variables sin inconsistencias en las dimensiones de sus vectores,
                   tampoco existan inconsistencias entre tales variables.'''
                subcampos_validados = list({'alpha', 'beta', 'sigma', 'e0'}.intersection(subcampos) - set(n_params['error']))
                Nombres = ''.join(i + ', ' for i in subcampos_validados[:-1])[:-2] + ' y ' + subcampos_validados[-1]
                shapes_validadas = []
                for s in subcampos_validados:
                    shapes_validadas.append(param[campo][s][0,0].shape)
                if not all(x == shapes_validadas[0] for x in shapes_validadas):
                    File.error('Existen inconsistencias en las dimensiones de los vectores entre los subcampos: ' + Nombres +\
                                  ' del ramo "' + campo + '". Favor de verificarlo.')
                    errores += 1
                else: # Se usa forma_Deuda para comparar contra la dimensión del vector "Kappa" del ramo "Spread"
                    forma_Deuda = shapes_validadas[0]
            elif campo == 'Spread' and len(subcampos) > 0:
                dim_kappa = []
                n_mercados[campo] = param[campo][subcampos[0]].shape[0]
                for s in subcampos:
                    for j in range(param[campo][s].shape[0]):
                        dim_kappa.append(param[campo][s][j,0].shape) # Dimensiones de cada matriz 'kappa'
                        try:
                            param[campo][s][j,0].astype(float64)
                        except ValueError:
                            File.error('El tipo de dato de la matriz (' + str(j+1) + ') en el subcampo "' + s +\
                                          '" de la rama "' + campo + '" no es de tipo flotante. Favor de verificarlo.')
                            errores += 1
                    '''Validando que todas las matrices sean de la misma dimensión'''
                    if s == 'kappa':
                        if not all(x == dim_kappa[0] for x in dim_kappa):
                            File.error('Existen inconsistencias en las dimensiones de los vectores de la variable: "' + s + \
                                '" del ramo "' + campo + '". Favor de verificarlo.')
                            errores += 1
                        else: # Se usa forma_Spread para comparar contra la dimensión de alpha,beta,sigma,e0 del ramo "Deuda"
                            forma_Spread = dim_kappa[0]
            elif campo == 'fechacorte':
                if not validaFec(param[campo][0],'%Y%m%d'):
                    File.warning('La fecha reportada en el ramo "' + campo + '" no es válida.')
            elif campo == 'Acciones' and len(subcampos) > 0:
                for s in subcampos:
                    for j in range(2):
                        if j == 0: # Columna 1: Tipo string
                            data = where(~vectorize(lambda t: isinstance(t[0],(str,str_)))(param[campo][s][:, 0]))[0]
                        else:      # Columna 2: Tipo entero
                            data = where(~vectorize(lambda t: isinstance(t[0,0],(int,int_,uint8)))(param[campo][s][:,1]))[0]
                        if len(data) > 0:
                            R = ''.join(str(data[i] + 1) + ', ' for i in range(len(data) - 1)) if len(data) > 1 else str(data[0]+1)
                            R = R[:-2] + ' y ' + str(data[-1] + 1) if len(data) > 1 else R
                            File.error('El subcampo "' + s + '" del ramo "' + campo + '" presenta inconsistencias de tipo' +\
                                          'de dato en los renglones : ' + R + '.')
                            errores += 1
            elif campo == 'Actuarial' and len(subcampos) > 0:
                for s in subcampos:
                    for llave in param[campo][s]: # Matriz-Matriz-Ramo
                        for j in range(param[campo][s][llave].shape[1]): # (1,6)
                            try:
                                param[campo][s][llave][0,j].astype(float64)
                            except ValueError:
                                File.error('La matriz ('+str(j+1)+') localizada en la rama "'+campo+'-'+\
                                              s+'-'+llave+'" del archivo no es de tipo flotante. Favor de verificarlo '+\
                                              'e intentar de nuevo.')
                                errores += 1
            else:  # Considerar los casos de las validaciones de: catRR4, Pensiones, Acciones y proveedor a futuro.
                pass

        if 'Deuda' in campos_validos and 'Spread' in campos_validos:
            '''Validación del mismo número de mercados entre "Deuda" y "Spread" si están en campos_validos'''
            ramo_mercados, nmercado = list(n_mercados.keys()), [str(i) for i in n_mercados.values()]
            Nombres = vectorize(lambda x,y: x +' ('+y+'), ')(ramo_mercados, nmercado)
            Nombres = ''.join(i for i in Nombres[:-1])[:-2] + ' y ' + Nombres[-1][:-2]
            if not all(x == nmercado[0] for x in nmercado):
                File.error('Existen inconsistencias en el número de mercados reportados para los siguientes ramos: '+Nombres+\
                              '. Favor de verificarlo e intentar de nuevo.')
                errores += 1
            '''Validación de la misma dimensión entre parámetros de "Deuda" y "Spread" si pasaron las validaciones previas'''
            if 'forma_Deuda' in locals() and 'forma_Spread' in locals():
                if forma_Deuda[0] != forma_Spread[0]:
                    File.error('La dimensión de los vectores de los parámetros existentes en el ramo "Deuda" (alpha,beta,sigma,e0) [' +\
                                  str(forma_Deuda[0])+'], no es consistente con la dimensión de los vectores del parámetro (kappa)' +\
                                  ' existente en el ramo "Spread" [' + str(forma_Spread[0]) + ']. Favor de verificarlo.')
                    errores += 1

    except (KeyError, ValueError, OSError, NotImplementedError):
        File.error('La estructura del archivo ' + str(rcs.par).split('/')[-1] + ' proporcionado como insumo "PARAMETROS.mat" no satisface los requerimientos. Favor de cargar nuevamente el archivo adecuado en el módulo "Carga de Archivos".')
        errores += 1

    '''Eliminando archivo log (File) del administrador'''
    logging.getLogger().removeHandler(File)
    logging.shutdown()

    '''Eliminando .log si está vacío'''
    if os.stat(namelog).st_size == 0:
        os.remove(namelog)

    bandera = 1 if errores == 0 else 0

    return bandera

def Campos(S1,S2,campo):
    """Función que valida los campos en común dados dos diccionarios.
       También detecta las diferencias entre estos.
       Devuelve una lista con los errores de inconsistencia encontrados
       y otra con aquellos subcampos en común para la rama 'campo'."""
    Error = []
    s1, s2 = set(S1[campo].keys()), set(S2[campo].keys())
    if len(s1-s2) > 0: # Llaves faltantes
        for c in list(s1-s2):
            Error.append('El subcampo "' + c + '" no se encuentra en la rama "' + campo + '" del archivo de '\
                         ' parámetros de referencia. Debe incluirse para proseguir con la validación de este insumo.')

    if len(s2-s1) > 0: # Llaves no reconocidas
        for c in list(s2-s1):
            Error.append('"' + c + '" no es un subcampo válido en la rama "' + campo + '" del archivo de '\
                          + ' parámetros de referencia. Favor de verificarlo y cargar nuevamente el archivo.')
    C = s1.intersection(s2)

    return Error, list(C)

def validaFec(fecha, formato):
    try:
        validacion = bool(datetime.strptime(fecha, formato))
    except ValueError:
        validacion = False

    return validacion

def voidTodict(void):
    """Función que recibe como insumo un objeto de tipo void, en este caso,
       utilizamos Layoutglobal y Parametros
       NOTA: Las llave 'Catalogo' y 'Reporte' de Parametros, contienen tablas
       que no son análogas a las de Matlab, por ello se han excluido."""
    D = {}
    for name in void.dtype.names:
        if name not in ['Catalogo', 'Reporte'] or void.dtype.names[0] != 'General':
            if void[name].dtype.names is None:
                D[name] = void[name]
            else:
                D[name] = voidTodict(void[name][0,0])
    return D

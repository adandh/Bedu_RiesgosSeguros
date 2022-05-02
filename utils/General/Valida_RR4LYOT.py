from numpy import float64, vectorize, unique, int_, where, uint8, str_, float_, delete, uint16, array, int64,\
    int32
from scipy.io import loadmat
from copy import deepcopy
import os.path
import logging

from utils.General.set_logger import set_logger


def Valida_RR4LYOT(rcs, dirErrores):
    """Función que se encarga de la validación general del insumo:
    RR4LYOTxxxxxyyyymmdd.mat"""

    ''' Variable que monitorea la existencia (o no) de errores'''
    errores = 0

    '''0. Archivo log donde se guardarán los posibles errores.'''
    Nombre = 'RR4LYOT' + rcs.fechacorte
    namelog = dirErrores + Nombre + '.log'  # Creación de archivo con errores en caso de existir errores.
    if os.path.isfile(namelog):
        os.remove(namelog)

    '''Creando archivo .log, asignando nivel ERROR y formato'''
    File = set_logger(Nombre, namelog, level=logging.WARN)

    try:
        '''Carga del archivo de parámetros de referencia'''
        Lyot = voidTodict(loadmat(rcs.lyot)['Layoutglobal'][0,0])

        '''Diccionario con nombres de campos esperados y su tipo de dato'''
        llaves = {'IRCAC': 'Flotante', # Todos flotantes/enteros
                'IRMES': 'Flotante',
                'IRVLP': 'Flotante',
                'AP': {'C': 'Flotante',
                       'I': 'Flotante'},
                'AutosF': {'Layout': 'Flotante'},
                'CPML': 'Flotante_Struct', # Estructura con flotantes
                'catReaseguroCPML': 'Str_Struct', # Estructura de strings
                'DivMiscel': {'Layout': 'Flotante'},
                'DivTec': {'Layout': 'Flotante'},
                'reaseguro': {'Layout': 'Flotante',
                              'catReaseguro': 'Str_Struct'},
                'GM': {'C': 'Flotante',
                       'I': 'Flotante'},
                'LAIRRea' : 'Flotante_Struct',
                'catReaseguroIRRea': 'Str_Struct',
                'Incendio': {'Layout': 'Flotante'},
                'ISME': {'Autos': {'F': {'cober_1':{'tipov3':{'RRC': 'Flotante',
                                                              'SONR': 'Flotante'}}}},
                         'DivMiscel': {'RRC': 'Flotante', 'SONR': 'Flotante'},
                         'DivTec': {'RRC': 'Flotante', 'SONR': 'Flotante'},
                         'Incendio' : {'RRC': 'Flotante', 'SONR': 'Flotante'},
                         'MarTrans': {'RRC': 'Flotante', 'SONR': 'Flotante'},
                         'RC': {'RRC': 'Flotante', 'SONR': 'Flotante'},
                         'AP': {'I': {'clase1':{'RRC': 'Flotante', 'SONR': 'Flotante'},
                                      'clase2':{'RRC': 'Flotante', 'SONR': 'Flotante'}},
                                'C': {'clase1':{'RRC': 'Flotante', 'SONR': 'Flotante'},
                                      'clase2':{'RRC': 'Flotante', 'SONR': 'Flotante'}}},
                         'GM': {'I':{'clase1':{'RRC': 'Flotante', 'SONR': 'Flotante'},
                                     'clase2':{'RRC': 'Flotante', 'SONR': 'Flotante'},
                                     'clase3':{'RRC': 'Flotante', 'SONR': 'Flotante'}},
                                'C':{'clase1':{'RRC': 'Flotante', 'SONR': 'Flotante'},
                                     'clase2':{'RRC': 'Flotante', 'SONR': 'Flotante'},
                                     'clase3':{'RRC': 'Flotante', 'SONR': 'Flotante'}}}},
                'MarTrans': {'Layout': 'Flotante'},
                'RC': {'Layout': 'Flotante'},
                'RO': 'Flotante',
                'ReaseguroTomado': {'Layout': 'Flotante'},
                'VidaCortoPlazo': {'Layout': {'datos': 'Flotante', 'llaveReaseguro': 'Flotante'}},
                'VLP':{'caducidad': 'Flotante',
                       'decrementos': {'mor': 'Flotante', 'acc': 'Flotante',
                                       'inv': 'Flotante', 'otr': 'Flotante'},
                       'P1': 'Flotante',
                       'VC': {'G': 'Flotante', 'kflujos': 'Flotante', 'P': 'Flotante'}},
                'CRED':{'act_sin_rcs': 'Struct_actsin'}, # Estructura de strings y numérica (Caso Especial actsin)
                'INMU':{'Cap': 'Struct_INMU'}, # Estructura de strings y numérica (Caso Especial INMU)
                'INVE':{'act_sin_rcs': 'Struct_actsin',
                        'ORC': 'Struct_ORC', # Estructura de strings y numérica (Caso Especial ORC)
                        'calificacion': 'Str_Struct',
                        'llave': 'Flotante',
                        'DEU': 'Struct_DEU', # Estructura de strings y numérica (Caso Especial DEU)
                        'CAP': 'Struct_CAP'}, # Estructura de strings y numérica (Caso Especial CAP)
                'OINV':{'act_sin_rcs': 'Struct_actsin', 'ORC': 'Struct_ORC'},
                'Financiero': {'Layout': {'Deu':{'T': 'Flotante', 'period_cpn': 'Flotante',
                                                 'tasa_fija_cpn_col': 'Flotante', 'titulo': 'Flotante',
                                                 'Vnominal_nAmort': 'Flotante', 'Valor_Mercado': 'Flotante',
                                                 'calif': 'Flotante',
                                                 'cadenaEmisor': 'Str_Struct', 'Serie': 'Str_Struct',
                                                 'TipoDeValor': 'Str_Struct', 'tasa_fija_cpn_val': 'Flotante',
                                                 'period_tasa_cpn': 'Flotante', 'curva_cpn': 'Flotante',
                                                 'curva_bono': 'Flotante', 'Emisor': 'Flotante',
                                                 'Amort': 'Flotante', 'NotaE': 'Flotante',
                                                 'PrestamoV': 'Flotante', 'SeguroF': 'Flotante',
                                                 'TasaG': 'Flotante', 'llave': 'Flotante',
                                                 'moneda_base': 'Flotante'},
                                          'Cap':{'Monto': 'Flotante', 'Titulos': 'Flotante',
                                                 'SeguroF': 'Flotante', 'TasaG': 'Flotante',
                                                 'moneda_base': 'Flotante', 'moneda': 'Flotante',
                                                 'Emisor': 'Str_Struct', 'Serie': 'Str_Struct',
                                                 'TipoV': 'Str_Struct', 'NotaE': 'Flotante',
                                                 'Indice': 'Flotante', 'Moneda': 'Flotante',
                                                 'clave_rep': 'Flotante'}}},
                'ORC':{'orc': 'Struct_ORC'},
                'act_sin_rcs': 'Struct_actsin'}

        '''Errores de nombre de campo y tipo de dato en el archivo RR4LYOT'''
        Faltantes_Datos = Intersect_Dict(llaves, Lyot, ruta_llave='RR4LYOT', tipo_error='Faltante',Errores=[],Dataerror=True,fechacorte=rcs.fechacorte)[1]
        Desconocidos = Intersect_Dict(Lyot, llaves, ruta_llave='RR4LYOT', tipo_error='Desconocido',Errores=[],Dataerror=False,fechacorte=rcs.fechacorte)[1]
        for error in Faltantes_Datos + Desconocidos:
            File.error(error)
            errores += 1

    except (KeyError, ValueError, OSError, NotImplementedError):
        File.error('La estructura del archivo ' + str(rcs.lyot).split('/')[-1] + ' proporcionado como insumo "RR4LYOT.mat" no satisface los requerimientos. Favor de cargar nuevamente el archivo adecuado en el módulo "Carga de Archivos".')
        errores += 1

    '''Eliminando archivo log (File) del administrador'''
    logging.getLogger().removeHandler(File)
    logging.shutdown()

    '''Eliminando .log si está vacío'''
    if os.stat(namelog).st_size == 0:
        os.remove(namelog)

    bandera = 1 if errores == 0 else 0

    return bandera

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

def Intersect_Dict(S1,S2,ruta_llave,tipo_error,Errores,Dataerror,fechacorte):
    """Devuelve un diccionario que contiene únicamente aquellas llaves cuyos
       nombres coinciden en su totalidad dados dos diccionarios. Además regresa
       una lista con los errores en caso de haberlos.
       Insumos:
       - S1: Diccionario guía
       - S2: Diccionario a validar
       - ruta_llave: Ruta inicial (Suele ser el nombre del archivo)
       - tipo_error: Puede ser Faltante/Campo_Desconocido dependiendo de si se está
                     validando que falten campos o que existan campos desconocidos
       - Errores: Lista donde se almacenan los errores, se suele dar vacía
       - Dataerror: Booleano. Si es True se incluyen errores del tipo de dato en Errores."""
    Dict_Int = {}
    Ramos = ['GM', 'AP', 'Salud', 'GM_H', 'RC', 'MarTrans', 'Incendio', 'AutosI', 'AutosF',
             'Credito', 'DivMiscel', 'DivTec', 'Caucion']
    for k in S1:
        'Se añade al diccionario de intersección solo la llave k si está en ambos'
        if k in S2:
            if len(S1[k]) > 0 and hasattr(S1[k],'keys'): # Existen subramas
                Dict_Int[k], Errores = Intersect_Dict(S1[k], S2[k], ruta_llave + '-' + k, tipo_error, Errores, Dataerror,fechacorte)
            else: # Rama terminal
                # print(ruta_llave + '-' + k,':',S2[k].shape) # Imprime rutas junto con la forma de S2[k] para checarlas
                Dict_Int[k] = {}
                if Dataerror:
                    if len(ruta_llave.split('-')) > 1 and ruta_llave.split('-')[1] in Ramos:
                        Dif = int(fechacorte[:4]) - S2[k][:, 0].astype(int)
                        if Dif.max() > 4:
                            Errores.append('Para la estructura ' + ruta_llave + '-' + k + ', existen registros con 5 o más años de ' + \
                                'antigüedad con respecto al reportado en la fecha de corte (' + fechacorte + ').' + \
                                           ' Favor de modificar la fecha de corte o la estructura.')
                        if Dif.min() < 0:
                            Errores.append('Para la estructura ' + ruta_llave + '-' + k + ', existen registros con año ' + \
                                'posterior al reportado en la fecha de corte (' + fechacorte + ').' + \
                                           ' Favor de modificar la fecha de corte o la estructura.')
                    if S1[k] == 'Flotante':
                        idR, idC = where(~vectorize(lambda t: isinstance(t,(float,float_,float64,int,int_,uint8,uint16)))(S2[k]))
                    elif S1[k] == 'Flotante_Struct':
                        idR, idC = where(~vectorize(lambda t: isinstance(t[0,0],(float,float_,float64,int,int_,uint8)))(S2[k]))
                    elif S1[k] == 'Str_Struct':
                        idR, idC = where(~vectorize(lambda t: isinstance(t[0],(str,str_)))(S2[k]))
                    elif S1[k] == 'Struct_actsin':
                        Struct_1, Struct_2 = delete(S2[k], 5, axis = 1), deepcopy(S2[k][:,[5]])
                        idR_1, idC_1 = where(~vectorize(lambda t: isinstance(t[0], (str, str_)))(Struct_1))
                        idR_2, idC_2 = where(~vectorize(lambda t: isinstance(t[0,0], (int, uint8, uint16)))(Struct_2))
                        if len(idC_1) > 0:
                            idC_1 = vectorize(lambda t: t if t <= 4 else t+1)(idC_1)
                        idC_2 += 5
                        idR, idC = array((list(idR_1)+list(idR_2)), dtype=int64), array((list(idC_1)+list(idC_2)), dtype=int64)
                    elif S1[k] == 'Struct_INMU':
                        Struct_1, Struct_2 = delete(S2[k], 41, axis=1), deepcopy(S2[k][:, [-1]])
                        idR_1, idC_1 = where(~vectorize(lambda t: isinstance(t[0],(str, str_)) if len(t) > 0 else True)(Struct_1))
                        idR_2, idC_2 = where(~vectorize(lambda t: isinstance(t[0,0],(int, uint8)))(Struct_2))
                        idC_2 += 41
                        idR, idC = array((list(idR_1)+list(idR_2)), dtype=int64), array((list(idC_1)+list(idC_2)), dtype=int64)
                    elif S1[k] == 'Struct_ORC':
                        DStruct_1 = {0:0, 1:1, 2:2, 3:5, 4:6, 5:8, 6:9, 7:12, 8:13, 9:14,
                                     10:15, 11:16, 12:17, 13:18}
                        DStruct_2 = {0:4, 1:7, 2:11}
                        DStruct_3 = {0:3, 1:10}
                        Struct_1 = delete(S2[k], [3,4,7,10,11,19], axis = 1)
                        Struct_2 = deepcopy(S2[k][:,[4,7,11]])
                        Struct_3 = deepcopy(S2[k][:,[3,10]])
                        Struct_4 = deepcopy(S2[k][:,[19]])
                        idR_1, idC_1 = where(~vectorize(lambda t: isinstance(t[0], (str, str_)))(Struct_1))
                        idR_2, idC_2 = where(~vectorize(lambda t: isinstance(t[0,0], (int, uint8, int32)))(Struct_2))
                        idR_3, idC_3 = where(~vectorize(lambda t: isinstance(t[0,0], (int32,float64,uint8)))(Struct_3))
                        idR_4, idC_4 = where(~vectorize(lambda t: isinstance(t[0,0], (uint8,uint16)))(Struct_4))

                        if len(idC_1) > 0: idC_1 = vectorize(lambda t: DStruct_1[t])(idC_1)
                        if len(idC_2) > 0: idC_2 = vectorize(lambda t: DStruct_2[t])(idC_2)
                        if len(idC_3) > 0: idC_3 = vectorize(lambda t: DStruct_3[t])(idC_3)
                        idC_4 += 19

                        idR = array((list(idR_1)+list(idR_2)+list(idR_3)+list(idR_4)), dtype=int64)
                        idC = array((list(idC_1)+list(idC_2)+list(idC_3)+list(idC_4)), dtype=int64)
                    elif S1[k] == 'Struct_DEU':
                        DStruct_1 = {i:i for i in range(33)}
                        DStruct_1.update({j:j+1 for j in range(33,63)})
                        DStruct_1.update({63:66})
                        DStruct_2 = {0:33, 1:64, 2:65}
                        Struct_1 = delete(S2[k], [33,64,65], axis=1)
                        Struct_2 = deepcopy(S2[k][:,[33,64,65]])
                        idR_1, idC_1 = where(~vectorize(lambda t: isinstance(t[0], (str, str_)))(Struct_1))
                        idR_2, idC_2 = where(~vectorize(lambda t: isinstance(t[0,0], (uint16, uint8)))(Struct_2))

                        if len(idC_1) > 0: idC_1 = vectorize(lambda t: DStruct_1[t])(idC_1)
                        if len(idC_2) > 0: idC_2 = vectorize(lambda t: DStruct_2[t])(idC_2)

                        idR = array((list(idR_1) + list(idR_2)), dtype=int64)
                        idC = array((list(idC_1) + list(idC_2)), dtype=int64)
                    elif S1[k] == 'Struct_CAP':
                        DStruct_1 = {i:i for i in range(64)}
                        DStruct_1.update({64:66})
                        DStruct_2 = {0:64, 1:65}
                        Struct_1 = delete(S2[k], [64,65], axis=1)
                        Struct_2 = deepcopy(S2[k][:,[64,65]])
                        idR_1, idC_1 = where(~vectorize(lambda t: isinstance(t[0], (str, str_)))(Struct_1))
                        idR_2, idC_2 = where(~vectorize(lambda t: isinstance(t[0,0], (uint16, uint8)))(Struct_2))

                        if len(idC_1) > 0: idC_1 = vectorize(lambda t: DStruct_1[t])(idC_1)
                        if len(idC_2) > 0: idC_2 = vectorize(lambda t: DStruct_2[t])(idC_2)

                        idR = array((list(idR_1) + list(idR_2)), dtype=int64)
                        idC = array((list(idC_1) + list(idC_2)), dtype=int64)
                    else: # Para otros casos aún no contemplados
                        idR, idC = array([], dtype = int64), array([], dtype = int64)
                    '''Añadimos errores existentes'''
                    if len(idR) > 0:
                        c_un, _, ic = unique(idC, axis=0, return_index=True, return_inverse=True)
                        for i in range(len(c_un)):
                            r = idR[where(ic == i)[0]]
                            R = ''.join(str(r[j] + 1) + ', ' for j in range(len(r) - 1)) if len(r) > 1 else str(
                                r[0] + 1)
                            R = R[:-2] + ' y ' + str(r[-1] + 1) if len(r) > 1 else R
                            Errores.append('La estructura ' + ruta_llave + '-' + k + ' presenta inconsistencias de tipo de dato ' + \
                                           'en la columna ' + str(c_un[i]+1) + ' en los renglones: '+ R + '.')
        else:
            if tipo_error == 'Faltante': # Campo faltante
                Errores.append('El campo "' + k + '" con ruta ' + ruta_llave + '-'+ k + ' no se encuentra en el insumo RR4LYOT.'\
                              + ' Debe incluirse para proseguir con la validación de este insumo.')
            else: # Campo desconocido
                Errores.append('El campo "' + k + '" con ruta ' + ruta_llave + '-'+ k + ' no es un campo válido en el insumo RR4LYOT.'\
                              + ' Favor de verificarlo y cargar nuevamente el archivo.')
    return Dict_Int, Errores
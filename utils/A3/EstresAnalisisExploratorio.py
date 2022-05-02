from pandas import DataFrame, read_excel
from seaborn import color_palette
from numpy import log
import matplotlib.pyplot as plt

from utils.General.primerP0 import primerP0


def EstresAnalisisExploratorio(rcs, dirSalidas):
    """
    Procedimiento que implementa el analisis exploratorio de informacion de mercado historica (datos Bloomberg de cierre mensual)
    Se calculan los valores teoricos implicitos para la media, volatilidad y correlaciones de los cambios en los factores
    de riesgo bajo el modelo financiero del RCS, los cuales se comparan con las estimaciones muestrales obtenidas para ventanas
    moviles con 5 anios de historia (mensual, trimestral, anual)
    """

    print('Inicio Estres Analisis Exploratorio con inicializacion')
    ## INICIALIZACION DE PARAMETROS GENERALES ((CONFORME AL SCRIPT Calculos_ResyReq_app Y PROCEDIMIENTOS DE CADA MODELO))    
    t = rcs.horizonte_riesgo      # Horizonte de riesgo
    n = rcs.numero_escenarios      # Numero de escenarios (Verificar consistencia con el Conjunto de Prueba y con el de Resultados de Simulaciones)

    # NIVEL DE CONFIANZA DE LAS METRICAS DE RIESGO

    tiposCurva=('BonosM','UMS','UDIBonos','TBills')
    tiposIndice=('USD','UDI','IPCconsumo','IPCmateriales','IPCindustrial','IPCfinanciero','IPCtelecom','IPCconsumoNF','IPC','FIBRAS','IBonosMex','ViviendaSHF','SPglobal1200')#DE ACUERDO CON EL ORDEN IMPLICITO DE NOTAS METODOLOGICAS 
    grupo=('BonosM yields','UMS yields','UDIBonos yields','TBills yields','FX rates (USD and UDI)','Equity indexes (S&P and IPC sectors)','Other indexes')
    plazos=(.25,.5,1,2,3,4,5,6,7,8,9,10,15,20,30)#VECTOR DE PLAZOS (NODOS) DE LAS CURVAS MEDIDOS EN ANIOS: PLAZOS CONSISTENTES CON LAS COLUMNAS Y ORDEN DE LA BD
    nC=len(plazos)*len(tiposCurva)#TOTAL DE PLAZOS ASOCIADOS A CURVAS CONSIDERADAS
    #NOTA: estoy dejando los indices igual pero hay que checar efecto de indexacion iniciada en cero para python
    idxG=(list(range(1,16)),list(range(16,31)),list(range(31,46)),list(range(46,61)),[nC+1,nC+2],[nC+13,nC+9,nC+3,nC+4,nC+5,nC+6,nC+7,nC+8],[nC+10,nC+11,nC+12])#COLUMNAS EN BD ASOCIADOS A CADA GRUPO DE FACTORES: NODOS TASAS + TIPOS CAMBIO + INDICES BURSATILES 


    # 0.2. ANALISIS DE ESTIMACIONES (MOVILES) DE PARAMETROS CON INFORMACION HISTORICA   
    #CARGA DE ARCHIVO CON INFORMACION HISTORICA DE CIERRE MENSUAL (BD): CURVAS DE TASAS, TIPOS DE CAMBIO E INDICES BURSATILES (BLOOMBERG)
    tabla = read_excel(rcs.info_mercado, index_col=0, parse_dates=True)
    tabla = DataFrame(tabla)
    tabla = tabla.rename_axis('Date')
    fecha = list(tabla.index.values)
    nombre = list(tabla.columns.values) 
     
    tabla.iloc[:,0:nC] = log(1+tabla.iloc[:,0:nC]/100) #CURVAS DE TASAS SPOT (BonosM,UMS,UDIBonos,TBills): EFECTIVA ANUAL (BLOOMBERG) 

    colores = ['#000000','#101010','#202020','#303030','#404040','#505050','#606060','#696969','#787878','#888888','#989898','#A8A8A8','#B0B0B0','#BEBEBE','#C8C8C8']
    color_dic = {0:dict(zip(list(range(1,16)), colores)),
             1:dict(zip(list(range(16,31)), colores)),
             2:dict(zip(list(range(31,46)), colores)),
             3:dict(zip(list(range(46,61)), colores)),
             4:{61:'#000000',62:'#888888'}}

    for i in range(len(grupo)):
        if(i<=4):
            tabla.loc[:,[nombre[j-1] for j in idxG[i]]].plot(color = [color_dic[i].get(x,'#333333') for x in idxG[i]], figsize=(20, 10))
            plt.legend(loc = 'center left', bbox_to_anchor = (1, .5), fontsize = 'small')
        else:
            aux_1=100*tabla.loc[:,[nombre[j-1] for j in idxG[i]]]/primerP0(tabla.loc[:,[nombre[j-1] for j in idxG[i]]])
            aux_1.plot(figsize=(20, 10))
            plt.legend(loc = 'center left', bbox_to_anchor = (1, .5), fontsize = 'small')
        plt.savefig(dirSalidas+'Series Mensuales [' + grupo[i] + '].png')


    # MEDIA Y VOLATILIDAD DE LOS CAMBIOS EN LOS FACTORES DE RIESGO SOBRE VENTANAS MOVILES 
    tabla.iloc[:,nC:] = log(tabla.iloc[:,nC:]) #USO DE PRECIOS LOGARITMICOS   
    nV=60 #LONGITUD VENTANA MOVIL EN MESES (OBSERVACIONES CONSECUTIVAS UTILIZADAS PARA CALCULOS DE MONITOREO)  
    nH=[12,3,1] #HORIZONTE DE RIESGO EN MESES (NUMERO DE REZAGOS UTILIZADOS PARA LAS DIFERENCIAS) 
    horizonte='[12m(warm), 3m(cool), 1m(gray) risk horizons]'
    colorTeo = '#ff00ff' #COLOR MAGENTA
    #CALCULO DE VALORES DE MEDIA Y VOLATILIDAD TEORICOS SOBRE HORIZONTE ANUAL (0,1)  
    #muC, sigmaC= Modificado_covImplicitaRplazo(1,(.25,.5,1,2,3,4,5,6,7,8,9,10,15,20,30),rcs)[0:2]
    #muTeo = muC
    #sigmaTeo = sigmaC
    #[muF,sigmaF] = Modificado_covImplicitaFactores(1,-1,rcs)[0:2] #LOS PRIMEROS FACTORES CORRESPONDEN A LAS TASAS SPOT DE LOS 4 MERCADOS
    #muTeo = hstack((muTeo,muF[4:]))
    #sigmaTeo = hstack((sigmaTeo,sigmaF[4:]))
    
    #ESTIMACIONES MUESTRALES DE MEDIA Y VOLATILIDAD SOBRE VENTANAS MOVILES 
    muRoll    = dict()
    sigmaRoll = dict()

    for g in range(len(grupo)):
        colores={"Rojos": color_palette("Reds_r",len(idxG[g])+5), "Azules": color_palette("Blues_r",len(idxG[g])+5), "Grises": color_palette("Greys_r",len(idxG[g])+5)}
        muRoll[g] = dict()
        sigmaRoll[g] = dict()
        for h in range(len(nH)):
            muRoll[g][h] = tabla.loc[:,[nombre[i-1] for i in idxG[g]]].diff(periods = nH[h]).rolling(nV).mean().loc[fecha[nV:],:]
            muRoll[g][h] = muRoll[g][h].rename(columns = lambda x: x + ' [' + str(nH[h]) + 'm]')
            sigmaRoll[g][h] = tabla.loc[:,[nombre[i-1] for i in idxG[g]]].diff(periods = nH[h]).rolling(nV).std().loc[fecha[nV:],:]
            sigmaRoll[g][h] = sigmaRoll[g][h].rename(columns = lambda x: x + ' [' + str(nH[h]) + 'm]')
        ax = muRoll[g][0].iloc[:,0].plot(figure=plt.figure(), color = colores["Rojos"], title = grupo[g] + ': 5-year rolling Mean ' + horizonte, linewidth = 2, figsize=(20, 10))
        #Series(data = muTeo[idxG[g][0]-1], index = fecha[nV:], name = 'Theoretical').plot(color = colorTeo, linewidth = 2)
        muRoll[g][0].iloc[:,1:].plot(ax = ax, color = colores["Rojos"], linewidth = .5)
        muRoll[g][1].iloc[:,0].plot(ax = ax, color = colores["Azules"], linewidth = 2)
        muRoll[g][1].iloc[:,1:].plot(ax = ax, color = colores["Azules"], linewidth = .5)
        muRoll[g][2].iloc[:,0].plot(ax = ax, color = colores["Grises"], linewidth = 2)
        muRoll[g][2].iloc[:,1:].plot(ax = ax, color = colores["Grises"], linewidth = .5)
        plt.legend(loc = 'center left', bbox_to_anchor = (1, .5), fontsize = 'small')
        plt.savefig(dirSalidas+'Media Muestral Ventanas Moviles [' + grupo[g] + '].png')
        ax = sigmaRoll[g][0].iloc[:,0].plot(figure=plt.figure(), color = colores["Rojos"], title = grupo[g] + ': 5-year rolling Volatility ' + horizonte, linewidth = 2, figsize=(20, 10))
        #Series(data = sigmaTeo[idxG[g][0]-1], index = fecha[nV:], name = 'Theoretical').plot(color = colorTeo, linewidth = 2)
        sigmaRoll[g][0].iloc[:,1:].plot(ax = ax, color = colores["Rojos"], linewidth = .5)
        sigmaRoll[g][1].iloc[:,0].plot(ax = ax, color = colores["Azules"], linewidth = 2)
        sigmaRoll[g][1].iloc[:,1:].plot(ax = ax, color = colores["Azules"], linewidth = .5)
        sigmaRoll[g][2].iloc[:,0].plot(ax = ax, color = colores["Grises"], linewidth = 2)
        sigmaRoll[g][2].iloc[:,1:].plot(ax = ax, color = colores["Grises"], linewidth = .5)
        plt.legend(loc = 'center left', bbox_to_anchor = (1, .5), fontsize = 'small')
        plt.savefig(dirSalidas+'Volatilidad Muestral Ventanas Moviles [' + grupo[g] + '].png')


"""estres middleware"""

import os, django
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")
django.setup()
#from django.conf import settings

#from RiesgosSeguros.settings import MEDIA_ROOT

from utils.A3.EstresAnalisisExploratorio import  EstresAnalisisExploratorio


# Se definen funciones que implementan el proceso de calculo principal (intensivo) por tipo de analisis
# Las funciones calculo_xxxx() llaman a funciones que realizan calculos via scripts (funciones en Python, Matlab o R) contenidos
# en las subcarpetas de 'utils'

def calculos_A3_Exploratorio(rcs, path_results):
    #Aqui se mandan a llamar la funciones que python que se necesitan ejecutar (similar a lo que hace el script principal)
    ts = time.time()
    print("Estoy en estres:middleware:calculos_A3_Exploratorio")
    EstresAnalisisExploratorio(rcs, path_results)
    tiempo_tot = time.time() - ts
    print(tiempo_tot)
    print("Fin de calculos_A3_Exploratorio")

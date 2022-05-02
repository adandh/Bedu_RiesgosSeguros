"""reportes views"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


## 1. Modulo Reporte 1 (Diario Final)
@login_required
def mainReporte1(request):
    print('Estoy en reportes:views:mainReporte1')
    return render(request, 'reportes/mainReporte1.html', {})


## 2. Modulo Reporte 2 (Riesgo Mercado)
@login_required
def mainReporte2(request):
    print('Estoy en reportes:views:mainReporte2')
    return render(request, 'reportes/mainReporte2.html', {})


## 3. Modulo Reporte 3 (Crédito INVE)
@login_required
def mainReporte3(request):    
    print('Estoy en reportes:views:mainReporte3')
    return render(request, 'reportes/mainReporte3.html', {})


## 4. Modulo Reporte 4 (Límites Portafolio)
@login_required
def mainReporte4(request):    
    print('Estoy en reportes:views:mainReporte4')
    return render(request, 'reportes/mainReporte4.html', {})


## 5. Modulo Reporte 5 (Cifras Control)
@login_required
def mainReporte5(request):    
    print('Estoy en reportes:views:mainReporte5')
    return render(request, 'reportes/mainReporte5.html', {})

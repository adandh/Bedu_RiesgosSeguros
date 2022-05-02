"""sensibilidad views"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


## 1. Modulo Sensibilidad Activo
@login_required
def mainSensibilidadActivo(request):
    print('Estoy en sensibilidad:views:mainSensibilidadActivo')
    return render(request, 'sensibilidad/mainSensibilidadActivo.html', {})


## 2. Modulo Sensibilidad Balance
@login_required
def mainSensibilidadBalance(request):
    print('Estoy en Sensibilidad:views:mainSensibilidadBalance')
    return render(request, 'sensibilidad/mainSensibilidadBalance.html', {})


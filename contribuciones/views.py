"""contribuciones views"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


## 1. Modulo Contribuciones al RCS de Activos
@login_required
def mainActivo(request):
    print('Estoy en contribuciones:views:mainActivo')
    return render(request, 'contribuciones/mainActivo.html', {})


## 2. Modulo Contribuciones al RCS de Balance
@login_required
def mainBalance(request):
    print('Estoy en contribuciones:views:mainActivo')
    return render(request, 'contribuciones/mainBalance.html', {})
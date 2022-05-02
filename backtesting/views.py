"""backtesting views"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def mainBacktesting(request):
    print('Estoy en backtesting:views:mainBacktesting')
    return render(request, 'backtesting/mainBacktesting.html', {})

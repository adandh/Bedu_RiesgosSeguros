"""portal views"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):	
	contexto={}	
	return render(request, 'portal/index.html', contexto)

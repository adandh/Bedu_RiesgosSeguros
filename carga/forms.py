from __future__ import unicode_literals

from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from carga.models import *


# Aqui se definen las variable que se pondran en el formulario, en templates se le da el formato en html de como se presentaran estas variables.
class CargaArchivosForm(forms.ModelForm):

    class Meta:
        model = CargaArchivosModel

        fields = [
                "lyot",
                "sim",
                "ref",
                "par",
                "lylp",
        ]
        labels = {
            "lyot":"RR4LYOT.mat",
            "sim":"RR4RSIM.mat",
            "ref":"referencia.mat",
            "par":"parametros.mat",
            "lylp":"RR4LYLP.mat",
        }
        widgets = {
            "lyot":forms.FileInput(attrs={"accept":".mat"}),
            "sim":forms.FileInput(attrs={"accept":".mat"}),
            "ref":forms.FileInput(attrs={"accept":".mat"}),
            "par":forms.FileInput(attrs={"accept":".mat"}),
            "lylp":forms.FileInput(attrs={"accept":".mat"}),
        }


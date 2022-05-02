"""estres forms"""

from django import forms

from estres.models import *


class EstresForm(forms.ModelForm):

    class Meta:
        model = EstresModel

        fields = [              
                "numero_escenarios",
                "horizonte_riesgo",
                "fechacorte",
                "info_mercado",
                "inc_financiero",
                "inc_biometricos",
                "inc_frecsev",
        ]
        labels = {
                "numero_escenarios":"Número de escenarios (entero de 1000 a 10000)",
                "horizonte_riesgo":"Horizonte de riesgo",
                "fechacorte":"Fecha de corte",
                "info_mercado":"INFO_MERCADO.xlsx",
                "inc_financiero":"INC_FINANCIERO.xlsx",                
                "inc_biometricos":"INC_BIOMETRICOS.xlsx",                
                "inc_frecsev":"INC_FRECUENCIA_SEVERIDAD.xlsx",                
        }
        widgets = {
                "numero_escenarios":forms.TextInput(),
                "horizonte_riesgo":forms.Select(),
                "fechacorte":forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'datepicker'}),
                "info_mercado":forms.FileInput(attrs={"accept":".xlsx"}),
                "inc_financiero":forms.FileInput(attrs={"accept":".xlsx"}),
                "inc_biometricos":forms.FileInput(attrs={"accept":".xlsx"}),
                "inc_frecsev":forms.FileInput(attrs={"accept":".xlsx"}),
        }



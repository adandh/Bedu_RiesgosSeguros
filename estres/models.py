"""estres models"""

import time

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


#Horizontes de riesgo
HORIZONTES_OP = {
    (1,"anual"),
    (1/12,"mensual"),
    (1/52,"semanal"),
    (1/252,"diario"),
}

#Ruta a la cual se carga el archivo insumo
def user_directory_path(instance, filename):
    print((instance, filename))
    return 'uploads/user_{0}_{2}/{1}'.format(instance.owner.username, filename, time.time())


#Se define el modelo de insumos (base de datos) principal
class EstresModel(models.Model):

    longitud_maxima = 1000 # Longitud maxima de la cadena del nombre de los insumos (incluyendo ruta asociada)

    folio = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User, related_name='rcs_est_owner', null=True, on_delete=models.CASCADE)
    date_insert = models.DateTimeField(default=timezone.now)
    date_update = models.DateTimeField(default=timezone.now)
    date_init = models.DateTimeField(verbose_name='Fecha de inicio',  null=True)
    date_end = models.DateTimeField(verbose_name='Fecha de fin', null=True)
    numero_escenarios = models.IntegerField(blank=True, default=1000, validators=[MinValueValidator(1000), MaxValueValidator(10000)])
    horizonte_riesgo = models.FloatField(blank=True, default=1, choices=HORIZONTES_OP)
    q = models.FloatField(default=.995, validators=[MinValueValidator(.00001), MaxValueValidator(.99999)])
    reprocesar = models.BooleanField(default=True)
    estres = models.BooleanField(default=False)
    compania = models.CharField(null=False, max_length=5, default='S0003')
    fechacorte = models.CharField(blank=True, null=False, max_length=100, default=timezone.now)
    val_reaseguro = models.BooleanField(default=True)
    aisla_P0 = models.BooleanField(default=False, null=True)
    nPlazo = models.IntegerField(default=35, validators=[MinValueValidator(5), MaxValueValidator(100)])
    rCredito = models.BooleanField(default=True)
    rMercado = models.BooleanField(default=True)

    sim = models.FileField(
        verbose_name='SIM.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    lyot = models.FileField(
        verbose_name='LYOT.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    lylp = models.FileField(
        verbose_name='LYLP.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    ref = models.FileField(
        verbose_name='REF.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    par = models.FileField(
        verbose_name='PAR.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    info_mercado = models.FileField(
        verbose_name='INFO_MERCADO.xlsx',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    inc_financiero = models.FileField(
        verbose_name='INC_FINANCIERO.xlsx',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    inc_biometricos = models.FileField(
        verbose_name='INC_BIOMETRICOS.xlsx',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    inc_frecsev = models.FileField(
        verbose_name='INC_FRECSEV.xlsx',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )

    def __str__(self):
        return str (self.owner.username) + " - " + str (self.id) + " - " + str (self.folio) 


#Se define el modelo de los resultados
class ResultadosEstres(models.Model):
    folio = models.CharField(max_length=100, null=False)
    rcs_est = models.ForeignKey(EstresModel, related_name='rcs_est', null=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=1000, null=False)
    zip_file = models.CharField(max_length=1000, null=False)
    date_create = models.DateTimeField(default=timezone.now)    


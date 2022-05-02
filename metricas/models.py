"""metricas models"""

import time

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


#Horizontes de riesgo
HORIZONTES_OP = {
    (1/12,"mensual"),
    (1/52,"semanal"),
    (1,"anual"),
    (1/252,"diario"),
}

#Ruta a la cual se carga el archivo insumo
def user_directory_path(instance, filename):
    print((instance, filename))
    return 'uploads/user_{0}_{2}/{1}'.format(instance.owner.username, filename, time.time())


#Se define el modelo de insumos (base de datos) principal
class MetricasRiesgoModel(models.Model):
    
    longitud_maxima = 1000 # Longitud maxima de la cadena del nombre de los insumos (incluyendo ruta asociada)

    #Definir cada una de las variables de entrada
    folio = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User, related_name='met_ries_owner', null=True, on_delete=models.CASCADE)
    date_insert = models.DateTimeField(default=timezone.now)
    date_update = models.DateTimeField(default=timezone.now)
    date_init = models.DateTimeField(verbose_name='Fecha de inicio',  null=True)
    date_end = models.DateTimeField(verbose_name='Fecha de fin', null=True)
    numero_escenarios = models.IntegerField(default=10000, validators=[MinValueValidator(1000), MaxValueValidator(10000)])
    # IMPORTANTE: Asignar valor predeterminado t=1 a horizonte_riesgo (para evitar efectos de escalamiento no deseado en llamadas iniciales a Modificado_Inicializacion_MetricasRiesgoEstandar.py)
    horizonte_riesgo = models.FloatField(blank=True, default=1, choices=HORIZONTES_OP)
    q = models.FloatField(default=.995, validators=[MinValueValidator(.00001), MaxValueValidator(.99999)])
    reprocesar = models.BooleanField(default=True)
    estres = models.BooleanField(default=False)
    compania = models.CharField(null=False, max_length=5, default='S0003')
    fechacorte = models.CharField(null=False, max_length=100, default=timezone.now)
    val_reaseguro = models.BooleanField(default=False) # SI TOMA EL VALOR default=True, SE REQUIERE DEL INSUMO lyot (EL ARCHIVO 'LYOT.mat' ES NECESARIO PARA PROCESAR 'RR4IMPREC.txt' RELATIVO A IMPORTES RECUPERABLES DE REASEGURO)
    aisla_P0 = models.BooleanField(default=False)
    nPlazo = models.IntegerField(blank=True, default=35, validators=[MinValueValidator(1), MaxValueValidator(100)])
    rCredito = models.BooleanField(default=True)
    rMercado = models.BooleanField(default=True)
    inflacion = models.FloatField(blank=True, default=.035)
    bps = models.FloatField(blank=True, default=100)
    columnas_compl = models.BooleanField(default=False)
    cartera_BT = models.BooleanField(default=True)
    ruta_Layout = models.CharField(blank=True, max_length=longitud_maxima, default='')
    ruta_DeuCamb = models.CharField(blank=True, max_length=longitud_maxima, default='')
    ruta_VectorPrecios = models.CharField(blank=True, max_length=longitud_maxima, default='')
    ruta_Parametros = models.CharField(blank=True, max_length=longitud_maxima, default='')
    excluye_Capitales_NO_PiP = models.BooleanField(default=True)
    excluye_Deuda_califD = models.BooleanField(default=True)
    horizonte_Diario = models.BooleanField(default=True)
    horizonte_Semanal = models.BooleanField(default=False)
    horizonte_Mensual = models.BooleanField(default=True)
    horizonte_Anual = models.BooleanField(default=True)

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
    cat = models.FileField(
        verbose_name='CATREA.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    vec = models.FileField(
        verbose_name='VECcnsf.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    rr7port = models.FileField(
        verbose_name='RR7Portafolios.xlsx',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    catcalif = models.FileField(
        verbose_name='CatalogoCalificacionesPIP.xlsx',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    vecpip = models.FileField(
        verbose_name='VectorPIP.xls',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    curpip = models.FileField(
        verbose_name='CurvasPIP.xls',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    rr7inmu = models.FileField(
        verbose_name='RR7EFTRINMU.txt',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    rr4imprec = models.FileField(
        verbose_name='RR4IMPREC.txt',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )
    histocurvas = models.FileField(
        verbose_name = 'histocurvas.csv',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path
        )
    histocurvasReportes = models.FileField(
        verbose_name = 'histocurvasReportes.csv',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path
        )
    histospread = models.FileField(
        verbose_name = 'histospread.csv',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path
        )
    histoTC = models.FileField(
        verbose_name = 'histoTC.csv',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path
        )
    histoVaR_Subgrupos = models.FileField(
        verbose_name = 'histoVaR_Subgrupos.csv',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path
        )
    histoVaR_Instrumentos = models.FileField(
        verbose_name = 'histoVaR_Instrumentos.csv',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path
        )


    def __str__(self):
        return str (self.owner.username) + " - " + str (self.id) + " - " + str (self.folio) 


#Se define el modelo de los resultados
class ResultadosMetricasRiesgo(models.Model):
    folio = models.CharField(max_length=100, null=False)
    met_ries = models.ForeignKey(MetricasRiesgoModel, related_name='met_ries', null=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=1000, null=False)
    zip_file = models.CharField(max_length=1000, null=False)
    date_create = models.DateTimeField(default=timezone.now) 


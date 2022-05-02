from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


#Se definen todos los menus asociados a las variable que se definiran en el modelo mas abajo
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    print((instance, filename))
    return 'uploads/'+'user_{0}/carga_archivos/{1}'.format(instance.owner.username, filename)

# Modelos (base de datos) de la aplicacion, donde se definen las variables, el tipo de variables, opciones de respuesta, default etc)
# Aqui se pueden definir todas las variables de utilidad relevantes, que pueden o no emplearse en el formulario.
class CargaArchivosModel(models.Model):

    longitud_maxima = 1000 # Longitud maxima de la cadena del nombre de los insumos (incluyendo ruta asociada)

    #Definir cada una de las variables de entrada
    folio = models.CharField(max_length=100, null=False)
    owner = models.ForeignKey(User, related_name='rcs_ca_owner', null=True, on_delete=models.CASCADE)
    date_insert = models.DateTimeField(default=timezone.now)
    date_update = models.DateTimeField(default=timezone.now)
    date_init = models.DateTimeField(verbose_name='Fecha de inicio',  null=True)
    date_end = models.DateTimeField(verbose_name='Fecha de fin', null=True)
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
    lylp = models.FileField(
        verbose_name='LYLP.mat',
        blank=True,
        null=True,
        max_length=longitud_maxima,
        upload_to=user_directory_path,
        )

    def __str__(self):
        return str (self.owner.username) + " - " + str (self.id) + " - " + str (self.folio) 


#Se define el modelo de los resultados
class ResultadosCargaArchivos(models.Model):
    folio = models.CharField(max_length=100, null=False)
    rcs = models.ForeignKey(CargaArchivosModel, related_name='rcs_ca', null=True, on_delete=models.CASCADE)
    path = models.CharField(max_length=1000, null=False)
    zip_file = models.CharField(max_length=1000, null=False)
    date_create = models.DateTimeField(default=timezone.now)


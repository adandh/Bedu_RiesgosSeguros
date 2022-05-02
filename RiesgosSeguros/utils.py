import datetime
import smtplib
import os
import time
import shutil
import zipfile
from email.mime.text import MIMEText
from email import encoders
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

from django.conf import settings


#Params gmail server and email accounts
mail_server = 'smtp.gmail.com:587'
from_addr = 'micorreo@gmail.com'  # IMPORTANTE: CONFIGURAR DIRECCION DE CORREO


# Credentials email
username = 'micorreo@gmail.com'  # IMPORTANTE: CONFIGURAR DIRECCION DE CORREO
password = 'micontrasena'  # IMPORTANTE: CONFIGURAR CONTRASEÑA


# 1) Envio de correo de resultados

def send_mail(email, url_resultados, carpeta_zip, analisis_solicitado, fecha_solicitud, insumos_especificos, rcs):  
    themsg = MIMEMultipart()
    themsg['Subject'] = ('Resultados - Riesgos de Seguros: "{0}"[{1}_{2}]'.format(analisis_solicitado, rcs.owner.username, rcs.id))
    themsg['To'] = email #", ".join(to_addr)
    themsg['From'] = from_addr
    
    # Construccion de bloques de mensaje html relativo a insumos y parametros utilizados 
    bloque_inicio = '''
        <html>
            <head></head>
            <body>
                <br>
                    <h3>El análisis solicitado mediante la aplicación web Riesgos de Seguros ha terminado.</h3>
                <br>
                <p>
                    <h4>I. Datos IDENTIFICACION:</h4>
                </p>
                <p>
                    Módulo: %s
                </p>
                <p>
                    Usuario: %s
                </p>
                <p>
                    Fecha de solicitud: %s
                </p>
                <p>
                    Folio: %s
                </p>
    ''' % (analisis_solicitado, rcs.owner.username, fecha_solicitud, rcs.id)

    bloque_insumos_especificos = '''
                <p>
                    <h4>I. Insumos ESPECIFICOS:</h4>
                </p>
    '''
    for elementos in insumos_especificos.items():
        if len(str(elementos[1]).strip()) > 0:
            bloque_insumos_especificos += '''
                <p>
                    %s: %s
                </p>
            ''' % elementos

    insumos_generales = (etiquetaInsumo(str(rcs.par).split('/')[-1]),
                          etiquetaInsumo(str(rcs.lyot).split('/')[-1]),
                          etiquetaInsumo(str(rcs.lylp).split('/')[-1]),
                          etiquetaInsumo(str(rcs.sim).split('/')[-1]),
                        )

    bloque_insumos_generales = '''
                <p>
                    <h4>II. Insumos GENERALES:</h4>
                </p>
                <p>
                    Archivo parametros.mat: %s
                </p>
                <p>
                    Archivo RR4LYOT.mat: %s
                </p>
                <p>
                    Archivo RR4LYLP.mat: %s
                </p>
                <p>
                    Archivo RR4SIM.mat: %s
                </p>
                <p>
    ''' % insumos_generales


    url_descarga = "http://127.0.0.1:8000/" + url_resultados

    bloque_fin = '''
                <br>
                    <h3>
                        Puede obtener los resultados mediante el enlace de descarga: <a href="%s">Resultados</a href>
                    </h3>
                <br>
                <p>
                    Gracias!
                </p>
            </body>
        </html>
    ''' % url_descarga

    html = bloque_inicio + bloque_insumos_especificos + bloque_insumos_generales + bloque_fin

    # Escritura de mensaje html en archivo .html para efectos de control de peticiones
    archivo_detalle_insumos = settings.ZIPS_ROOT + 'DetalleInsumos_' + carpeta_zip + ".html"
    with open(archivo_detalle_insumos,'w') as htmlDetalle:
        htmlDetalle.write(html)

    # Incorporacion de archivo .html a la carpeta .zip de resultados
    archivo_resultados_zip = settings.ZIPS_ROOT + carpeta_zip + ".zip"
    with zipfile.ZipFile(archivo_resultados_zip, 'a') as zipResultados:
        zipResultados.write(archivo_detalle_insumos, os.path.basename(archivo_detalle_insumos))
        os.remove(archivo_detalle_insumos)

    # Envio de correo electronico en internet via SMTP (Simple Mail Transfer Protocol)
    part1 = MIMEText(html, 'html', 'utf-8')
    themsg.attach(part1)    
    server = smtplib.SMTP(mail_server)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_addr, email, str(themsg))
    server.quit()
    print('Email Resultados OK')


# 2) Envio de correo de notificacion

def send_mail_notificacion(email, analisis_solicitado, fecha_solicitud, insumos_especificos, rcs):  
    themsg = MIMEMultipart()
    themsg['Subject'] = ('Solicitud - Riesgos de Seguros: "{0}"[{1}_{2}]'.format(analisis_solicitado, rcs.owner.username, rcs.id))
    themsg['To'] = email #", ".join(to_addr)
    themsg['From'] = from_addr
    
    # Construccion de bloques de mensaje html relativo a insumos y parametros utilizados 
    bloque_inicio = '''
        <html>
            <head></head>
            <body>
                <br>
                    <h3>El análisis solicitado mediante la aplicación web Riesgos de Seguros está siendo procesado.</h3>
                <br>
                <p>
                    <h4>I. Datos IDENTIFICACION:</h4>
                </p>
                <p>
                    Módulo: %s
                </p>
                <p>
                    Usuario: %s
                </p>
                <p>
                    Fecha de solicitud: %s
                </p>
                <p>
                    Folio: %s
                </p>
    ''' % (analisis_solicitado, rcs.owner.username, fecha_solicitud, rcs.id)

    bloque_insumos_especificos = '''
                <p>
                    <h4>I. Insumos ESPECIFICOS:</h4>
                </p>
    '''
    for elementos in insumos_especificos.items():
        if len(str(elementos[1]).strip()) > 0:
            bloque_insumos_especificos += '''
                <p>
                    %s: %s
                </p>
            ''' % elementos

    insumos_generales = (etiquetaInsumo(str(rcs.par).split('/')[-1]),
                          etiquetaInsumo(str(rcs.lyot).split('/')[-1]),
                          etiquetaInsumo(str(rcs.lylp).split('/')[-1]),
                          etiquetaInsumo(str(rcs.sim).split('/')[-1]),
                        )

    bloque_insumos_generales = '''
                <p>
                    <h4>II. Insumos GENERALES:</h4>
                </p>
                <p>
                    Archivo parametros.mat: %s
                </p>
                <p>
                    Archivo RR4LYOT.mat: %s
                </p>
                <p>
                    Archivo RR4LYLP.mat: %s
                </p>
                <p>
                    Archivo RR4SIM.mat: %s
                </p>
                <p>
    ''' % insumos_generales

    bloque_fin = '''
                <br>
                    <h3>
                        Se le notificará por este medio cuando los resultados estén disponibles.
                    </h3>
                <br>
                <p>
                    Gracias!
                </p>
            </body>
        </html>
    '''

    html = bloque_inicio + bloque_insumos_especificos + bloque_insumos_generales + bloque_fin

    # Envio de correo electronico en internet via SMTP (Simple Mail Transfer Protocol)
    part1 = MIMEText(html, 'html', 'utf-8')
    themsg.attach(part1)    
    server = smtplib.SMTP(mail_server)
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(from_addr, email, str(themsg))
    server.quit()
    print('Email Solicitud OK')



def zip_out(name_file, path_result):
    print (path_result)
    shutil.make_archive(settings.ZIPS_ROOT + name_file, 'zip', path_result)
    return settings.ZIPS_ROOT + name_file + ".zip"


def etiquetaInsumo(cadena):
    return cadena if len(cadena)>0 else '"No considerado"'

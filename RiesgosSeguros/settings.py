"""Django settings for RiesgosSeguros project"""

#from pathlib import Path
import os
from django.urls import reverse_lazy

#BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'django-insecure-aehj__f1%)68nc-@b-p9l5(&a0e46!-c5ne&(8j(g2a6hbzxm@'
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'portal',
    'metricas',
    'contribuciones',
    'estres',
    'carga',
    'salida',
    'sensibilidad',
    'backtesting',
    'reportes',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'RiesgosSeguros.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'RiesgosSeguros.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization

LANGUAGE_CODE = 'es-mx'

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_L10N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)

#STATIC_ROOT = 'static'
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_ROOT = BASE_DIR + '/media/'
RESULTS_ROOT = MEDIA_ROOT + 'results/'
ZIPS_ROOT = MEDIA_ROOT + 'zips/'


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Authentication

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = reverse_lazy('portal:index') 
LOGOUT_REDIRECT_URL = reverse_lazy('login')


# Celery

CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = 'django-cache'


# Logs de errores general y para cada aplicacion

LOG_FILE =  BASE_DIR + '/../log/rcs.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(funcName)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FILE ,
            'when': 'midnight', # this specifies the interval
            'interval': 1, # defaults to 1, only necessary for other values 
            'backupCount': 10, # how many backup file to keep, 10 days
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,            
        },
        'portal': {
            'handlers': [ 'file'],
            'level': 'WARNING',
            'propagate': True,            
        },
        'metricas': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'contribuciones': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,            
        },
        'estres': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,            
        },
       'salida': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,            
        },
        'carga': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
        'RiesgosSeguros': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}


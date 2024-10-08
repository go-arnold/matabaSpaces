from pathlib import Path
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-g^np^jf$2$s^=bll*fhwe*3+i=h@fwv6udhevmfj%3tab40^v5'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-g^np^jf$2$s^=bll*fhwe*3+i=h@fwv6udhevmfj%3tab40^v5')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = os.environ.get('DEBUG', 'False') == 'True'


#ALLOWED_HOSTS = ['127.0.0.1','172.20.10.12','localhost', '192.168.1.73','192.168.1.85','cikuru-spaces-k6fz.onrender.com',]
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'park.apps.ParkConfig',
    'authentication.apps.AuthenticationConfig',
    'reservation.apps.ReservationConfig',
    'stats.apps.StatsConfig',
    
    'dbbackup',
]
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/restore/'}

AUTH_USER_MODEL = 'authentication.User'
#AUTHENTICATION_BACKENDS = ['authentication.backends.EmailBackend']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_FROM = 'verify.matabaspaces@gmail.com'
EMAIL_FROM = 'arnoldciku@gmail.com'
#EMAIL_HOST_USER = 'verify.matabaspaces@gmail.com'
EMAIL_HOST_USER = 'arnoldciku@gmail.com'
#EMAIL_HOST_PASSWORD ='qnmgivorllkiujig'  
EMAIL_HOST_PASSWORD ='raizdlbsugophphs'  
EMAIL_PORT = 587
EMAIL_USE_TLS = True

PASSWORD_RESET_TIMEOUT=300


# project_name/settings.py
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Africa/Kigali'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
   'whitenoise.middleware.WhiteNoiseMiddleware',
   
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
   
]


"""
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),)
"""
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images')





ROOT_URLCONF = 'matabaSpaces.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'matabaSpaces.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

"""  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}  """
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'defaultdb',
        'USER': 'avnadmin',
        'PASSWORD': 'AVNS_2pz-of7L39sXYdZB_ve',
        'HOST': 'cikuruspaces-cikuruspaces.d.aivencloud.com',
        'PORT': '17101',
    }
}
"""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'defaultdb'),
        'USER': os.environ.get('DB_USER', 'avnadmin'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'AVNS_2pz-of7L39sXYdZB_ve'),
        'HOST': os.environ.get('DB_HOST', 'cikuruspaces-cikuruspaces.d.aivencloud.com'),
        'PORT': os.environ.get('DB_PORT', '17101'),
    }
}




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Kigali'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/




# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'




#APPEND_SLASH = False


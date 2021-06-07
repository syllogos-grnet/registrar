"""
Django settings for syllogos project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Custom logger please
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'cli': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  os.environ.get(
    'SYLLOGOS_SECRET_KEY'
) or'ptmfxdo3q3*$3dei=tox1kz#i_kw=3@kpinx3d5-gub$6g^o@@'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('SYLLOGOS_DEBUG') or False

ALLOWED_HOSTS = os.environ.get('SYLLOGOS_ALLOWED_HOSTS', '').split(',') or []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'syndromes.apps.SyndromesConfig'
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

ROOT_URLCONF = 'syllogos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'syllogos.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'el'

TIME_ZONE = 'EET'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.environ.get('SYLLOGOS_STATIC_ROOT') or '.'
STATIC_URL = '/static/'


# Setup email
EMAIL_HOST = os.environ.get("SYLLOGOS_EMAIL_HOST") or ""
EMAIL_PORT = int(os.environ.get("SYLLOGOS_EMAIL_PORT") or 25)
_default_email_backend = "django.core.mail.backends.dummy.EmailBackend"
EMAIL_BACKEND = os.environ.get(
    "SYLLOGOS_EMAIL_BACKEND") or _default_email_backend

# Member email limits
# How many consequtive emails can be sent to the same address
EMAILS_LIMIT = int(os.environ.get("SYLLOGOS_EMAILS_LIMIT", 3))
# In seconds
RESET_EMAILS_LIMIT_AFTER = int(os.environ.get(
    "SYLLOGOS_RESET_EMAILS_LIMIT_AFTER", 600))

# Default from and recepients
EMAIL_FROM = os.environ.get("SYLLOGOS_EMAIL_FROM") or "ds-syllogos@grnet.gr"

_notify_subject = "[Σύλλογος Ε&Σ ΕΔΥΤΕ] Ενημέρωση συνδρομών"
NOTIFY_SUBJECT = os.environ.get("SYLLOGOS_NOTIFY_SUBJECT") or _notify_subject

_notify_message = """
Αγαπητό μέλος του συλλόγου,

έχετε εγγραφεί στο σύλλογο ως «{name}».
Σύμφωνα με τα αρχεία μας, οφείλετε {dept:.2f} ευρώ.

Μπορείτε να εξοφλήσετε το χρέος σας με κατάθεση στον τραπεζικό λογαριασμό του
συλλόγου και να ενημερώσετε άμεσα με email το ΔΣ του Συλλόγου
( {from_email} )

Ο λογαριασμός του Συλλόγου
---
Εθνική Τράπεζα της Ελλάδας
IBAN: GR4401107210000072110088977
ΣΥΛΛΟΓΟΣ ΕΡΓΑΖΟΜΕΝΩΝ ΚΑΙ ΣΥΝΕΡΓΑΤΩΝ ΕΔΥΤΕ

Σε περίπτωση κατάθεσης με κόστος συναλλαγής (π.χ. από διαφορετική τράπεζα), θα
πρέπει να επωμισθείτε τις σχετικές τραπεζικές χρεώσεις, διαφορετικά το κόστος
αυτό θα προστεθεί ως χρέος σας προς το σύλλογο.

Αν πιστεύετε ότι έχει γίνει κάποιο λάθος, επικοινωνήστε με το ΔΣ του Συλλόγου
ώστε να βρεθεί το πρόβλημα.

Αυτό το email αποστέλεται αυτόματα,
με ευθύνη του ΔΣ του Συλλόγου Εργαζομένων και Συνεργατών ΕΔΥΤΕ
"""
NOTIFY_MESSAGE = os.environ.get("SYLLOGOS_NOTIFY_MESSAGE") or _notify_message

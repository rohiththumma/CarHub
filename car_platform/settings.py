# File: car_platform/settings.py

from pathlib import Path
import os
import dj_database_url # Import dj-database-url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- PRODUCTION SETTINGS ---
# SECRET_KEY should be set in an environment variable, not here.
SECRET_KEY = os.environ.get('SECRET_KEY', 'default-insecure-key-for-development')

# DEBUG must be False in production for security.
# We set it based on an environment variable. Render will not set this, so it will be False.
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# ALLOWED_HOSTS needs to know your Render URL.
# We get this from an environment variable Render provides.
ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# --- INSTALLED_APPS ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'listings',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # --- Add Whitenoise middleware ---
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'car_platform.urls'

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

WSGI_APPLICATION = 'car_platform.wsgi.application'

# --- DATABASE CONFIGURATION ---
# SQLite is not used in production. We will use PostgreSQL from Render.
# The DATABASE_URL environment variable will be provided by Render.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = 'static/'
# This is where collectstatic will gather all static files.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Tell Whitenoise to serve static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

# Email settings remain the same for now. You can configure a real email
# service later using environment variables.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
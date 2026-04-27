import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Support reading from environment variables (for Vercel/production)
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'django-insecure-REPLACE-WITH-YOUR-OWN-SECRET-KEY')

# Default DEBUG to False on Vercel, True locally unless explicitly set.
_is_vercel_runtime = bool(os.getenv('VERCEL'))
_debug_default = 'False' if _is_vercel_runtime else 'True'
DEBUG = os.getenv('DEBUG', _debug_default).lower() in ['true', '1', 'yes']

_env_allowed = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1')
# Split, strip and ignore empty entries
ALLOWED_HOSTS = [h.strip() for h in _env_allowed.split(',') if h.strip()]

# Always allow Vercel preview and deploy domains (any subdomain of vercel.app)
if '.vercel.app' not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append('.vercel.app')

# Also allow localhost variants for local testing if not present
for local_host in ('localhost', '127.0.0.1'):
    if local_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(local_host)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # our app
    'core.apps.CoreConfig',
    # ckeditor
    'ckeditor',
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

ROOT_URLCONF = 'school_site.urls'

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

WSGI_APPLICATION = 'school_site.wsgi.application'

# Database configuration - default to SQLite, can be overridden by environment
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# If DATABASE_URL environment variable is set, use PostgreSQL
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

_blob_token = os.getenv('BLOB_READ_WRITE_TOKEN', '').strip()
_blob_base_url = os.getenv('BLOB_BASE_URL', '').strip().rstrip('/')
if _blob_token:
    STORAGES = {
        'default': {
            'BACKEND': 'core.storage_backends.VercelBlobStorage',
        },
        'staticfiles': {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        },
    }
    if _blob_base_url:
        MEDIA_URL = f'{_blob_base_url}/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email is configured from the site settings admin page.
DEFAULT_FROM_EMAIL = 'Prime Choice Kids Care <noreply@localhost>'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

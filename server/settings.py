from pathlib import Path
import os

# ==========================
# Base settings
# ==========================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'  # production: use environment variable

DEBUG = True  # dev=True, prod=False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # add your domain in prod

# ==========================
# Installed apps
# ==========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks', 

    # Your apps
    'accounts',
    'students',
    'book',
    'inovice',
    'core',
]

# ==========================
# Middleware
# ==========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'server.urls'

# ==========================
# Templates
# ==========================
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

WSGI_APPLICATION = 'server.wsgi.application'

# ==========================
# Database (sqlite for dev)
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================
# Password validators
# ==========================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ==========================
# Auth settings
# ==========================
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = ''
LOGOUT_REDIRECT_URL = 'login'

# ==========================
# Internationalization
# ==========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dushanbe'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==========================
# Static files
# ==========================
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# ==========================
# Default auto field
# ==========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================
# Email backend (local dev)
# ==========================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ==========================
# Production-ready Email example (Gmail)
# ==========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'fbukhoriev8@gmail.com'
EMAIL_HOST_PASSWORD = 'fivv gcrv rmko vxhm'

# settings.py (extractos importantes)
import os
from pathlib import Path
import environ
from datetime import timedelta

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env'))  # apunta a D:\WEB_T\LOGIN\.env

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DJANGO_DEBUG')
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS').split(',')

# Apps
INSTALLED_APPS = [
    'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes',
    'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'rest_framework.authtoken',
    'corsheaders','axes','ratelimit','csp',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Database (Postgres)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Password hashing -> Argon2 first
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': int(env('PASSWORD_MIN_LENGTH', 12))}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Custom user model (if you will)
AUTH_USER_MODEL = 'core.User'

# REST Framework + JWT (SimpleJWT) settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from pathlib import Path
PRIVATE_KEY_PATH = env('JWT_PRIVATE_KEY_PATH')
PUBLIC_KEY_PATH = env('JWT_PUBLIC_KEY_PATH')
with open(PRIVATE_KEY_PATH, 'r') as f:
    JWT_PRIVATE_KEY = f.read()
with open(PUBLIC_KEY_PATH, 'r') as f:
    JWT_PUBLIC_KEY = f.read()

SIMPLE_JWT = {
    'ALGORITHM': env('JWT_ALGORITHM', default='RS256'),
    'SIGNING_KEY': JWT_PRIVATE_KEY,
    'VERIFYING_KEY': JWT_PUBLIC_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    # IMPORTANT: we'll implement custom blacklisting in Redis (see views)
}

# CSRF & cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SAMESITE = 'Lax'

# HTTPS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = False

# CSP
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")
CSP_BASE_URI = ("'self'",)

# Axes (brute-force)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 30  # minutes lockout
AXES_LOCKOUT_CALLABLE = 'core.utils.custom_lockout_response'  # optional custom handler

# Email (dev)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = int(env('EMAIL_PORT'))
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Redis config for blacklist & sessions
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

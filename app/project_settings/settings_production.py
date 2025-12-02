"""
Configuración para producción - Lista para dominio y SSL
"""
import os
from pathlib import Path
import environ

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False),
    SECURE_SSL_REDIRECT=(bool, True),
)

# Read .env file
environ.Env.read_env(os.path.join(BASE_DIR.parent, '.env.production'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG', default=False)

# Dominio de producción - AQUÍ PONES TU DOMINIO
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'tudominio.com',          # ← CAMBIA POR TU DOMINIO
    'www.tudominio.com',     # ← CAMBIA POR TU DOMINIO
    'tusubdominio.herokuapp.com',  # Si usas Heroku
    'tuip.publico',          # Tu IP pública si tienes
]

# ==================== SEGURIDAD EMPRESARIAL (YA IMPLEMENTADA) ====================

# Security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir archivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'axes.middleware.AxesMiddleware',  # Protección contra fuerza bruta
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SSL/HTTPS Configuration - PARA PRODUCCIÓN
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', default=True)  # Redirige HTTP → HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Cookies seguras
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# CORS para tu dominio
CORS_ALLOWED_ORIGINS = [
    'https://tudominio.com',      # ← CAMBIA POR TU DOMINIO
    'https://www.tudominio.com',  # ← CAMBIA POR TU DOMINIO
]

CSRF_TRUSTED_ORIGINS = [
    'https://tudominio.com',      # ← CAMBIA POR TU DOMINIO
    'https://www.tudominio.com',  # ← CAMBIA POR TU DOMINIO
]

# ==================== BASE DE DATOS PRODUCCIÓN ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST', default='localhost'),
        'PORT': env('POSTGRES_PORT', default='5432'),
    }
}

# ==================== ARCHIVOS ESTÁTICOS ====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'src', 'templates', 'frontend', 'assets'),
]

# WhiteNoise para servir archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================== EMAIL PRODUCCIÓN ====================
# Configuración real para envío de tokens
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = env('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL', default='noreply@tudominio.com')

# ==================== JWT PARA TOKENS ====================
from datetime import timedelta

# Rutas a tus claves reales (generadas para producción)
PRIVATE_KEY_PATH = env('JWT_PRIVATE_KEY_PATH', default='./private.pem')
PUBLIC_KEY_PATH = env('JWT_PUBLIC_KEY_PATH', default='./public.pem')

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
}

# ==================== REDIS PARA CACHÉ/BLACKLIST ====================
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{env('REDIS_HOST', default='localhost')}:{env('REDIS_PORT', default=6379)}/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# ==================== LOGGING PRODUCCIÓN ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}

# ==================== APPS (MANTENER TUS APPS) ====================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'axes',
    
    # Your apps
    'core',
]

# Resto de tu configuración (AUTH_PASSWORD_VALIDATORS, TEMPLATES, etc.)
# ... [Mantén el resto de tu configuración actual]

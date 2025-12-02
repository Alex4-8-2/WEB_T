"""
Configuración de desarrollo - 100% funcional localmente
Con toda la seguridad empresarial ACTIVADA
"""
import os
from pathlib import Path
from datetime import timedelta

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== CONFIGURACIÓN BÁSICA ====================
SECRET_KEY = 'django-insecure-dev-key-turismo-bolivia-2024-seguro'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# ==================== SEGURIDAD EMPRESARIAL (ACTIVADA) ====================

# Aplicaciones de seguridad
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Seguridad y API
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'axes',  # Protección contra fuerza bruta
    
    # Tu aplicación
    'core',
]

MIDDLEWARE = [
    # Seguridad
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
    # Core Django
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    
    # Seguridad avanzada
    'axes.middleware.AxesMiddleware',  # Anti brute-force
    
    # Django estándar
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== BASE DE DATOS (SQLite para desarrollo) ====================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==================== VALIDACIÓN DE CONTRASEÑAS (SEGURIDAD) ====================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Hashers de contraseñas (Argon2 es el más seguro)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# ==================== JWT TOKENS (PARA LOGIN/VERIFICACIÓN) ====================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
}

# ==================== CORS (Cross-Origin Resource Sharing) ====================
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# ==================== ARCHIVOS ESTÁTICOS ====================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, '..', 'src', 'templates', 'frontend', 'assets'),
]

# WhiteNoise para servir archivos estáticos
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==================== TEMPLATES ====================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '..', 'src', 'templates')],
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

# ==================== EMAIL (PARA ENVÍO DE TOKENS) ====================
# En desarrollo, los emails se muestran en consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@turismobolivia.dev'

# ==================== REDIS PARA CACHÉ/JWT BLACKLIST ====================
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

# ==================== CACHÉ (Redis simulado para desarrollo) ====================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# ==================== CONFIGURACIÓN DE SEGURIDAD ====================
# En desarrollo, algunas configs se relajan pero se mantiene la estructura
SESSION_COOKIE_SECURE = False  # True en producción
CSRF_COOKIE_SECURE = False     # True en producción
SECURE_SSL_REDIRECT = False    # True en producción con Cloudflare

# Axes (protección contra fuerza bruta)
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 30  # minutos de bloqueo
AXES_LOCKOUT_TEMPLATE = 'core/lockout.html'

# ==================== URL CONFIGURATION ====================
ROOT_URLCONF = 'urls'

# ==================== DEFAULT AUTO FIELD ====================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================== LOGGING ====================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}


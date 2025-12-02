# settings_local.py - Configuración temporal con SQLite
import os

# Usar SQLite en lugar de PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
    }
}

# Desactivar algunas dependencias que requieren PostgreSQL
INSTALLED_APPS_REMOVE = ['axes', 'django_redis']

# Configuración simplificada
DEBUG = True
ALLOWED_HOSTS = ['*']
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(os.path.dirname(__file__), '..', 'src', 'templates', 'frontend', 'assets')]
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'staticfiles')

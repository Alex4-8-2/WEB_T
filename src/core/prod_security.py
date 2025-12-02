# PRODUCCIÓN - SEGURIDAD MÍNIMA
DEBUG = False
SECRET_KEY = 'django-insecure-!cambiar-esta-clave-en-produccion!'

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Security middleware settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# Session security
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Para desarrollo local (quitar en producción real)
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000']

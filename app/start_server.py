import os
import sys
import django
from django.core.management.commands.runserver import Command as Runserver

# Configurar entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_settings.settings_development')

try:
    # Inicializar Django
    django.setup()
    print('✅ Django inicializado correctamente')
    
    # Obtener configuración
    from django.conf import settings
    print(f'• DEBUG: {settings.DEBUG}')
    print(f'• ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
    print(f'• STATIC_URL: {settings.STATIC_URL}')
    
    # Crear e iniciar servidor
    print('🚀 Iniciando servidor en http://localhost:8000')
    print('🛑 Para detener: Ctrl+C')
    print('=' * 60)
    
    # Ejecutar runserver directamente
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000', '--noreload'])
    
except Exception as e:
    print(f'❌ ERROR: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, '/app')
print(f"Python path: {sys.path}")

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
print(f"Django settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    import django
    print(f"Django version: {django.__version__}")
    django.setup()
    print("✅ Django configurado correctamente")
    
    # Probar modelos
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"✅ Modelo User cargado: {User}")
    
    # Contar usuarios
    user_count = User.objects.count()
    print(f"✅ Usuarios en la base de datos: {user_count}")
    
    # Probar conexión a base de datos
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print(f"✅ Conexión a PostgreSQL: {result}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

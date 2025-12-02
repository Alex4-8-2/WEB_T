import sys
import os

# Añadir /app al PYTHONPATH
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
    
    from django.contrib.auth import get_user_model
    User = get_user_model()
    print(f"✅ Modelo User: {User}")
    
    # Crear superusuario si no existe
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Superusuario creado: admin/admin123")
    else:
        print("ℹ️ Superusuario ya existe")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

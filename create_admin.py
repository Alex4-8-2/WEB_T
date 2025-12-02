import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("✅ Superusuario creado: admin/admin123")
    else:
        print("ℹ️ Superusuario ya existe")
except Exception as e:
    print(f"❌ Error: {e}")

#!/bin/bash

echo "=== INICIALIZACI?N DEL SISTEMA DE LOGIN ==="
echo ""

# Esperar a PostgreSQL
echo "1. Esperando a que PostgreSQL est? listo..."
sleep 15

# Aplicar migraciones
echo "2. Aplicando migraciones de Django..."
python manage.py migrate --noinput
echo "   ? Migraciones aplicadas"

# Crear superusuario si no existe
echo "3. Verificando/creando superusuario..."
python << EOF
import sys
sys.path.insert(0, "/app")
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@example.com", "admin123")
    print("? Superusuario creado: admin/admin123")
else:
    print("?? Superusuario ya existe")
EOF

# Iniciar servidor
echo ""
echo "4. Iniciando servidor Django..."
echo "   ?? URL: http://0.0.0.0:8000"
echo "   ?? Admin: http://0.0.0.0:8000/admin"
echo "   ?? Credenciales: admin / admin123"
echo "=========================================="
echo ""
exec python manage.py runserver 0.0.0.0:8000
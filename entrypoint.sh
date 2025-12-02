#!/bin/bash

# Esperar a que PostgreSQL esté listo
echo "Esperando a que PostgreSQL esté listo..."
until pg_isready -h postgres -p 5432 -U login_user; do
  sleep 2
  echo "Esperando PostgreSQL..."
done

echo "✅ PostgreSQL está listo!"

# Ejecutar migraciones
echo "Aplicando migraciones de Django..."
python manage.py migrate --noinput

# Crear superusuario si no existe
echo "Creando superusuario..."
python << EOF
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('Superusuario creado: admin/admin123')
    else:
        print('Superusuario ya existe')
except Exception as e:
    print(f'Error creando superusuario: {e}')
EOF

echo "✅ Inicialización completada!"
echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000

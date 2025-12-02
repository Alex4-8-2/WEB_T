#!/bin/bash

echo "=========================================="
echo "?? INICIANDO SISTEMA DE LOGIN"
echo "=========================================="

# Configurar Python path
export PYTHONPATH=/app

# Esperar PostgreSQL
echo "1. Esperando PostgreSQL..."
sleep 10

# Verificar si podemos conectar a PostgreSQL
echo "2. Verificando conexi?n a PostgreSQL..."
if python -c "
import psycopg2
import os
import time

try:
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB', 'login_system'),
        user=os.environ.get('POSTGRES_USER', 'login_user'),
        password=os.environ.get('POSTGRES_PASSWORD', 'login_password'),
        host=os.environ.get('POSTGRES_HOST', 'login_db'),
        port=os.environ.get('POSTGRES_PORT', '5432')
    )
    print('? Conectado a PostgreSQL')
    conn.close()
except Exception as e:
    print(f'? Error conectando a PostgreSQL: {e}')
    print('Intentando crear la base de datos...')
    try:
        # Conectar a la base de datos por defecto 'postgres' para crear la BD
        conn = psycopg2.connect(
            dbname='postgres',
            user=os.environ.get('POSTGRES_USER', 'login_user'),
            password=os.environ.get('POSTGRES_PASSWORD', 'login_password'),
            host=os.environ.get('POSTGRES_HOST', 'login_db'),
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f\"CREATE DATABASE {os.environ.get('POSTGRES_DB', 'login_system')};\")
        cursor.close()
        conn.close()
        print('? Base de datos creada')
    except Exception as e2:
        print(f'? Error creando base de datos: {e2}')
        exit(1)
"; then
    echo "   ? PostgreSQL listo"
else
    echo "   ? Error con PostgreSQL"
    exit 1
fi

# Aplicar migraciones
echo "3. Aplicando migraciones..."
python manage.py migrate

# Crear superusuario si no existe
echo "4. Creando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('  ? Superusuario creado: admin / admin123')
else:
    print('  ?? Superusuario ya existe')
"

# Iniciar servidor
echo "5. Iniciando servidor Django..."
echo "   ?? URL: http://0.0.0.0:8000"
echo "   ?? Admin: http://0.0.0.0:8000/admin"
echo "   ?? Credenciales: admin / admin123"
echo "=========================================="

exec python manage.py runserver 0.0.0.0:8000
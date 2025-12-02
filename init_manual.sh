#!/bin/sh

# Script de inicialización para Django
set -e

echo "=========================================="
echo "🚀 INICIANDO SISTEMA DE LOGIN - MANUAL"
echo "=========================================="

# 1. Esperar PostgreSQL
echo "1. Esperando PostgreSQL..."
sleep 10

# 2. Crear base de datos si no existe
echo "2. Verificando base de datos..."
python -c "
import psycopg2
import os
import time

max_retries = 30
retry_delay = 2

for i in range(max_retries):
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user=os.environ.get('POSTGRES_USER', 'login_user'),
            password=os.environ.get('POSTGRES_PASSWORD', 'login_password'),
            host=os.environ.get('POSTGRES_HOST', 'login_db'),
            port=os.environ.get('POSTGRES_PORT', '5432')
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute(\"SELECT 1 FROM pg_database WHERE datname='login_system';\")
        if not cursor.fetchone():
            print(f'  Creando base de datos login_system...')
            cursor.execute('CREATE DATABASE login_system;')
        
        cursor.close()
        conn.close()
        print('  ✅ Base de datos verificada/creada')
        break
    except Exception as e:
        if i < max_retries - 1:
            print(f'  ⏳ Reintentando conexión ({i+1}/{max_retries})...')
            time.sleep(retry_delay)
        else:
            print(f'  ❌ Error después de {max_retries} intentos: {e}')
            exit 1
"

# 3. Aplicar migraciones
echo "3. Aplicando migraciones..."
python manage.py migrate

# 4. Crear superusuario si no existe
echo "4. Creando superusuario..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('  ✅ Superusuario creado: admin / admin123')
else:
    print('  ℹ️ Superusuario ya existe')
"

# 5. Iniciar servidor
echo "5. Iniciando servidor Django..."
echo "   🌐 URL: http://0.0.0.0:8000"
echo "   👑 Admin: http://0.0.0.0:8000/admin"
echo "   🔐 Credenciales: admin / admin123"
echo "=========================================="

python manage.py runserver 0.0.0.0:8000

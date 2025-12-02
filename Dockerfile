FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias mínimas PERO necesarias
RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY ./src /app

# Crear init.sh MÁS simple
RUN echo '#!/bin/bash' > /init.sh && \
    echo 'echo "=== INICIANDO SISTEMA ==="' >> /init.sh && \
    echo 'sleep 10' >> /init.sh && \
    echo 'python manage.py migrate --noinput' >> /init.sh && \
    echo 'python manage.py shell -c "' >> /init.sh && \
    echo 'from django.contrib.auth import get_user_model' >> /init.sh && \
    echo 'User = get_user_model()' >> /init.sh && \
    echo 'if not User.objects.filter(username=\"admin\").exists():' >> /init.sh && \
    echo '    User.objects.create_superuser(\"admin\", \"admin@example.com\", \"admin123\")' >> /init.sh && \
    echo '    print(\"Superusuario creado\")' >> /init.sh && \
    echo 'else:' >> /init.sh && \
    echo '    print(\"Superusuario ya existe\")' >> /init.sh && \
    echo '"' >> /init.sh && \
    echo 'echo "Servidor: http://0.0.0.0:8000"' >> /init.sh && \
    echo 'exec python manage.py runserver 0.0.0.0:8000' >> /init.sh && \
    chmod +x /init.sh

EXPOSE 8000

CMD ["/bin/bash", "/init.sh"]

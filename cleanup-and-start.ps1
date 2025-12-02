# cleanup-and-start.ps1
Write-Host "🧹 Iniciando sistema de login..." -ForegroundColor Cyan

# Limpiar
docker-compose down -v
docker system prune -f

# Construir
docker-compose build --no-cache

# Iniciar
docker-compose up -d

# Esperar
Write-Host "⏳ Esperando 45 segundos..." -ForegroundColor Yellow
Start-Sleep -Seconds 45

# Verificar
docker-compose ps
docker-compose logs web --tail=20

Write-Host "`n✅ Sistema listo: http://localhost:8000" -ForegroundColor Green

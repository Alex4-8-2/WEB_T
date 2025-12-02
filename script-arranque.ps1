# script-arranque.ps1 - Usar este script para iniciar el sistema

# Ejecutar desde PowerShell:
# .\script-arranque.ps1

Write-Host "🚀 Iniciando sistema..." -ForegroundColor Cyan
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
Start-Sleep -Seconds 30
docker-compose logs web --tail=20

Write-Host "`n✅ Sistema listo en http://localhost:8000" -ForegroundColor Green

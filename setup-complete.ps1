Write-Host "=== CONFIGURACIÓN COMPLETA DEL SISTEMA DE LOGIN ===" -ForegroundColor Cyan
Write-Host "Fecha: $(Get-Date)" -ForegroundColor Gray
Write-Host ""

# 1. Detener servicios previos si existen
Write-Host "1. Limpiando servicios previos..." -ForegroundColor Yellow
docker-compose down 2>$null
Write-Host "   ✅ Servicios detenidos" -ForegroundColor Green

# 2. Construir imágenes
Write-Host "2. Construyendo imágenes Docker..." -ForegroundColor Yellow
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ Error construyendo imágenes" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Imágenes construidas" -ForegroundColor Green

# 3. Iniciar PostgreSQL y Redis
Write-Host "3. Iniciando base de datos y cache..." -ForegroundColor Yellow
docker-compose up -d postgres redis

# 4. Esperar a PostgreSQL
Write-Host "4. Esperando a que PostgreSQL esté listo..." -ForegroundColor White
$maxAttempts = 15
for ($i = 1; $i -le $maxAttempts; $i++) {
    try {
        $result = docker-compose exec -T postgres pg_isready -U login_user 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ PostgreSQL listo (intento $i/$maxAttempts)" -ForegroundColor Green
            break
        }
    } catch {}
    
    if ($i -eq $maxAttempts) {
        Write-Host "   ❌ PostgreSQL no responde después de $maxAttempts intentos" -ForegroundColor Red
        docker-compose logs postgres --tail=20
        exit 1
    }
    
    Write-Host "   ⏳ Esperando... ($i/$maxAttempts)" -ForegroundColor Gray
    Start-Sleep -Seconds 3
}

# 5. Configurar Django
Write-Host "5. Configurando Django..." -ForegroundColor Yellow
docker run --rm `
    --network login_default `
    -v "${PWD}/src:/app" `
    -w /app `
    python:3.12-slim `
    sh -c "
        echo 'Instalando dependencias...' &&
        pip install Django==4.2.7 psycopg2-binary==2.9.9 &&
        echo 'Aplicando migraciones...' &&
        python manage.py migrate --noinput &&
        echo 'Creando superusuario...' &&
        python -c \"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('✅ Superusuario creado')
    else:
        print('✅ Superusuario ya existe')
except Exception as e:
    print(f'ℹ️ Nota: {e}')
        \"
    "

if ($LASTEXITCODE -ne 0) {
    Write-Host "   ❌ Error configurando Django" -ForegroundColor Red
    exit 1
}
Write-Host "   ✅ Django configurado" -ForegroundColor Green

# 6. Iniciar todos los servicios
Write-Host "6. Iniciando todos los servicios..." -ForegroundColor Yellow
docker-compose up -d

# 7. Esperar inicialización
Write-Host "7. Esperando inicialización del servidor web..." -ForegroundColor White
Start-Sleep -Seconds 15

# 8. Verificar estado
Write-Host "8. Verificando estado..." -ForegroundColor Cyan
docker-compose ps

# 9. Mostrar información
Write-Host "`n=== SISTEMA CONFIGURADO EXITOSAMENTE ===" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 URLs DEL SISTEMA:" -ForegroundColor White
Write-Host "   • Aplicación:    http://localhost:8000" -ForegroundColor Cyan
Write-Host "   • Panel Admin:   http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host "   • PostgreSQL:    localhost:5432" -ForegroundColor Gray
Write-Host "   • Redis:         localhost:6379" -ForegroundColor Gray
Write-Host ""
Write-Host "🔑 CREDENCIALES:" -ForegroundColor White
Write-Host "   • Usuario: admin" -ForegroundColor Yellow
Write-Host "   • Contraseña: admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 COMANDOS ÚTILES:" -ForegroundColor White
Write-Host "   • Ver logs:       docker-compose logs -f" -ForegroundColor Gray
Write-Host "   • Detener:        docker-compose down" -ForegroundColor Gray
Write-Host "   • Reiniciar:      docker-compose restart" -ForegroundColor Gray
Write-Host "   • Estado:         docker-compose ps" -ForegroundColor Gray
Write-Host ""

# 10. Probar acceso
Write-Host "9. Probando acceso al sistema..." -ForegroundColor Yellow
$attempts = 0
$maxTestAttempts = 10
$success = $false

while ($attempts -lt $maxTestAttempts -and -not $success) {
    $attempts++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "   ✅ Sistema respondiendo correctamente (intento $attempts/$maxTestAttempts)" -ForegroundColor Green
            Write-Host "   📄 Contenido: $($response.Content.Substring(0, [Math]::Min(100, $response.Content.Length)))..." -ForegroundColor Gray
            $success = $true
        }
    } catch {
        if ($attempts -eq $maxTestAttempts) {
            Write-Host "   ⚠️  Sistema no responde aún. Intenta manualmente en unos segundos." -ForegroundColor Yellow
            Write-Host "   📋 Últimos logs del servidor:" -ForegroundColor Gray
            docker-compose logs web --tail=10
        } else {
            Write-Host "   ⏳ Intentando conexión... ($attempts/$maxTestAttempts)" -ForegroundColor DarkGray
            Start-Sleep -Seconds 5
        }
    }
}

Write-Host "`n🎉 ¡CONFIGURACIÓN COMPLETADA!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan

# test_website.ps1 - Script para probar el sitio web

Write-Host "🚀 INICIANDO PRUEBA DEL SITIO WEB" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# 1. Verificar que estamos en el directorio correcto
Write-Host "`n1. Verificando directorio..." -ForegroundColor White
if (-not (Test-Path "manage.py")) {
    Write-Host "   ❌ ERROR: No se encuentra manage.py" -ForegroundColor Red
    Write-Host "   Cambia al directorio del proyecto: cd D:\WEB_T\LOGIN" -ForegroundColor Yellow
    exit 1
}
Write-Host "   ✅ Directorio correcto" -ForegroundColor Green

# 2. Verificar Python
Write-Host "`n2. Verificando Python..." -ForegroundColor White
try {
    python --version
    Write-Host "   ✅ Python instalado" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python no encontrado" -ForegroundColor Red
    Write-Host "   Descarga Python: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

# 3. Ejecutar corrección de templates
Write-Host "`n3. Corrigiendo templates..." -ForegroundColor White
if (Test-Path "fix_static_refs.py") {
    python fix_static_refs.py
} else {
    Write-Host "   ⚠️  Script de corrección no encontrado" -ForegroundColor Yellow
}

# 4. Recolectar archivos estáticos
Write-Host "`n4. Recolectando archivos estáticos..." -ForegroundColor White
python manage.py collectstatic --noinput
Write-Host "   ✅ Archivos estáticos recolectados" -ForegroundColor Green

# 5. Verificar base de datos (si es necesario)
Write-Host "`n5. Verificando base de datos..." -ForegroundColor White
try {
    python manage.py migrate --check
    Write-Host "   ✅ Base de datos OK" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Necesitas configurar la base de datos" -ForegroundColor Yellow
    Write-Host "   Ejecuta: python manage.py migrate" -ForegroundColor Gray
    python manage.py migrate
}

# 6. Crear superusuario si no existe
Write-Host "`n6. Verificando superusuario..." -ForegroundColor White
try {
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('   Usuarios:', User.objects.count())"
} catch {
    Write-Host "   ⚠️  ¿Quieres crear un superusuario?" -ForegroundColor Yellow
    Write-Host "   Ejecuta: python manage.py createsuperuser" -ForegroundColor Gray
}

# 7. INICIAR SERVIDOR
Write-Host "`n🎉 TODO LISTO!" -ForegroundColor Green -BackgroundColor DarkGreen
Write-Host "`n🌐 INICIANDO SERVIDOR EN:" -ForegroundColor Cyan
Write-Host "   http://localhost:8000" -ForegroundColor White
Write-Host "   http://127.0.0.1:8000" -ForegroundColor White
Write-Host "`n📌 URLs importantes:" -ForegroundColor Cyan
Write-Host "   • Página principal: http://localhost:8000" -ForegroundColor Gray
Write-Host "   • Admin Django: http://localhost:8000/admin" -ForegroundColor Gray
Write-Host "   • Archivos estáticos: http://localhost:8000/static/assets/" -ForegroundColor Gray
Write-Host "`n🛑 Para detener el servidor: Presiona Ctrl+C" -ForegroundColor Yellow
Write-Host "`n⏳ Iniciando servidor en 5 segundos..." -ForegroundColor Yellow

Start-Sleep -Seconds 5

# Iniciar servidor
Write-Host "`n🚀 SERVIDOR INICIADO - Abre tu navegador en http://localhost:8000" -ForegroundColor Green
python manage.py runserver 0.0.0.0:8000

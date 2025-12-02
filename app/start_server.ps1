# Cambiar al directorio correcto
cd "D:\WEB_T\LOGIN\app"

# Ruta de Python
$python = "C:\Users\Alexander\AppData\Local\Programs\Python\Python314\python.exe"

Write-Host "=== INICIANDO SERVIDOR DJANGO ===" -ForegroundColor Cyan
Write-Host "Directorio: $(Get-Location)" -ForegroundColor Green

# Verificar dependencias básicas
Write-Host "`n1. Verificando Django..." -ForegroundColor White
try {
    & $python -c "import django; print(f'Django version: {django.__version__}')"
} catch {
    Write-Host "   Instalando Django..." -ForegroundColor Yellow
    & $python -m pip install django
}

# Migrar base de datos si es necesario
Write-Host "`n2. Configurando base de datos..." -ForegroundColor White
& $python manage.py migrate

# Recolectar archivos estáticos
Write-Host "`n3. Recolectando archivos estáticos..." -ForegroundColor White
& $python manage.py collectstatic --noinput

# Crear superusuario si no existe (opcional)
Write-Host "`n4. ¿Crear superusuario para admin? (S/N)" -ForegroundColor Yellow
$response = Read-Host "   Respuesta"
if ($response -eq 'S' -or $response -eq 's') {
    & $python manage.py createsuperuser
}

# INICIAR SERVIDOR
Write-Host "`n🚀 SERVIDOR LISTO!" -ForegroundColor Green -BackgroundColor DarkGreen
Write-Host "`n🌐 URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "   Admin: http://localhost:8000/admin" -ForegroundColor Cyan
Write-Host "`n🛑 Para detener: Presiona Ctrl+C" -ForegroundColor Yellow
Write-Host "`n⏳ Iniciando servidor..." -ForegroundColor Gray

& $python manage.py runserver 0.0.0.0:8000

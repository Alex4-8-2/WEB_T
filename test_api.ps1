Write-Host "=== PRUEBA DEL SISTEMA DE AUTENTICACIÓN ===" -ForegroundColor Cyan

# 1. Probar login
try {
    $loginData = @{
        username = "admin"
        password = "admin123"
    } | ConvertTo-Json
    
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" `
        -Method POST `
        -Headers @{"Content-Type" = "application/json"} `
        -Body $loginData `
        -ErrorAction Stop
    
    Write-Host "✅ Login exitoso!" -ForegroundColor Green
    Write-Host "   Access Token: $($loginResponse.access.Substring(0, 30))..." -ForegroundColor Gray
    Write-Host "   Refresh Token: $($loginResponse.refresh.Substring(0, 30))..." -ForegroundColor Gray
    
    # Guardar token para pruebas posteriores
    $global:accessToken = $loginResponse.access
    
} catch {
    Write-Host "❌ Error en login: $($_.Exception.Message)" -ForegroundColor Red
}

# 2. Probar verificación de token
if ($global:accessToken) {
    try {
        $checkResponse = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/check/" `
            -Method POST `
            -Headers @{
                "Content-Type" = "application/json"
                "Authorization" = "Bearer $global:accessToken"
            } `
            -ErrorAction Stop
        
        Write-Host "✅ Token verificado correctamente" -ForegroundColor Green
        Write-Host "   Usuario: $($checkResponse.user.username)" -ForegroundColor Gray
        Write-Host "   Email: $($checkResponse.user.email)" -ForegroundColor Gray
        
    } catch {
        Write-Host "⚠️  Error verificando token: $($_.Exception.Message)" -ForegroundColor Yellow
    }
}

# 3. Probar rutas disponibles
Write-Host "`n=== RUTAS DISPONIBLES ===" -ForegroundColor Cyan
Write-Host "• Login: POST http://localhost:8000/api/auth/login/" -ForegroundColor White
Write-Host "• Refresh Token: POST http://localhost:8000/api/auth/token/refresh/" -ForegroundColor White
Write-Host "• Registro: POST http://localhost:8000/api/auth/register/" -ForegroundColor White
Write-Host "• Logout: POST http://localhost:8000/api/auth/logout/" -ForegroundColor White
Write-Host "• Verificar: POST http://localhost:8000/api/auth/check/" -ForegroundColor White
Write-Host "• Perfil: GET http://localhost:8000/api/users/profile/" -ForegroundColor White
Write-Host "• Documentación: http://localhost:8000/swagger/" -ForegroundColor White

Write-Host "`n✅ Sistema configurado exitosamente!" -ForegroundColor Green

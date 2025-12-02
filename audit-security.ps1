# SECURITY AUDIT SCRIPT FOR DJANGO PROJECT - FIXED VERSION
# =========================================================

Write-Host ""
Write-Host "ANALIZADOR DE SEGURIDAD DJANGO" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Variables
$score = 0
$maxScore = 100
$checks = @()
$settingsFile = ".\src\core\settings.py"
$urlsFile = ".\src\core\urls.py"
$dockerComposeFile = ".\docker-compose.yml"
$requirementsFile = ".\requirements.txt"

# Function to add check
function Add-Check {
    param(
        [string]$Description,
        [bool]$Passed,
        [int]$Weight,
        [string]$Message
    )
    
    $check = [PSCustomObject]@{
        Description = $Description
        Passed = $Passed
        Weight = $Weight
        Message = $Message
    }
    
    $global:checks += $check
    
    if ($Passed) {
        $global:score += $Weight
    }
}

# Function to check if string exists in file
function Test-FileContains {
    param(
        [string]$FilePath,
        [string]$Pattern
    )
    
    if (Test-Path $FilePath) {
        $content = Get-Content $FilePath -Raw
        return $content -match $Pattern
    }
    return $false
}

# Function to check Django version
function Get-DjangoVersion {
    if (Test-Path $requirementsFile) {
        $content = Get-Content $requirementsFile
        $djangoLine = $content | Where-Object { $_ -match "^Django==" }
        if ($djangoLine) {
            return $djangoLine.Split('=')[-1]
        }
    }
    return "Unknown"
}

# ======================
# 1. DJANGO SETTINGS CHECKS
# ======================

Write-Host "ANALIZANDO CONFIGURACION DJANGO..." -ForegroundColor Yellow

# Check 1: DEBUG mode
$debugEnabled = Test-FileContains -FilePath $settingsFile -Pattern "DEBUG\s*=\s*True"
Add-Check -Description "DEBUG desactivado en produccion" -Passed (!$debugEnabled) -Weight 15 `
    -Message $(if ($debugEnabled) {"DEBUG=True detectado - RIESGO ALTO"} else {"DEBUG=False o no encontrado"})

# Check 2: Secret Key handling
$secretKeyHardcoded = Test-FileContains -FilePath $settingsFile -Pattern "SECRET_KEY\s*=\s*['\""].*['\""]"
Add-Check -Description "Secret Key desde variables de entorno" -Passed (!$secretKeyHardcoded) -Weight 10 `
    -Message $(if ($secretKeyHardcoded) {"Secret Key hardcodeada - RIESGO"} else {"Secret Key desde env vars"})

# Check 3: Allowed Hosts
$hasAllowedHosts = Test-FileContains -FilePath $settingsFile -Pattern "ALLOWED_HOSTS"
$allowedHostsProper = Test-FileContains -FilePath $settingsFile -Pattern "ALLOWED_HOSTS\s*=\s*\[\s*['\""].*['\""]\s*\]|ALLOWED_HOSTS\s*=\s*\[\s*['\""]\*['\""]\s*\]"
Add-Check -Description "ALLOWED_HOSTS configurado correctamente" -Passed ($hasAllowedHosts -and !$allowedHostsProper) -Weight 10 `
    -Message $(if (!$hasAllowedHosts) {"ALLOWED_HOSTS no configurado"} elseif ($allowedHostsProper) {"ALLOWED_HOSTS muy permisivo"} else {"ALLOWED_HOSTS configurado"})

# Check 4: CSRF Protection
$csrfEnabled = Test-FileContains -FilePath $settingsFile -Pattern "'django\.middleware\.csrf\.CsrfViewMiddleware'"
Add-Check -Description "CSRF Protection habilitado" -Passed $csrfEnabled -Weight 8 `
    -Message $(if ($csrfEnabled) {"CSRF habilitado"} else {"CSRF deshabilitado"})

# Check 5: Security Middleware
$securityMiddleware = Test-FileContains -FilePath $settingsFile -Pattern "'django\.middleware\.security\.SecurityMiddleware'"
Add-Check -Description "Security Middleware habilitado" -Passed $securityMiddleware -Weight 5 `
    -Message $(if ($securityMiddleware) {"Security Middleware activo"} else {"Security Middleware faltante"})

# Check 6: X-Content-Type-Options
$hasContentTypeOptions = Test-FileContains -FilePath $settingsFile -Pattern "SECURE_CONTENT_TYPE_NOSNIFF"
Add-Check -Description "X-Content-Type-Options configurado" -Passed $hasContentTypeOptions -Weight 5 `
    -Message $(if ($hasContentTypeOptions) {"Configuracion de headers seguros"} else {"Headers de seguridad no configurados"})

# Check 7: HTTPS/SSL settings
$hasHttpsSettings = Test-FileContains -FilePath $settingsFile -Pattern "SECURE_SSL_REDIRECT|SECURE_PROXY_SSL_HEADER"
Add-Check -Description "Configuracion HTTPS/SSL" -Passed $hasHttpsSettings -Weight 8 `
    -Message $(if ($hasHttpsSettings) {"Configuracion HTTPS presente"} else {"Configuracion HTTPS recomendada"})

# Check 8: Database password in settings
$dbPasswordPlain = Test-FileContains -FilePath $settingsFile -Pattern "PASSWORD\s*:\s*['\"].*['\"]"
Add-Check -Description "Credenciales DB desde variables de entorno" -Passed (!$dbPasswordPlain) -Weight 10 `
    -Message $(if ($dbPasswordPlain) {"Password DB hardcodeado - RIESGO"} else {"DB config desde env vars"})

# ======================
# 2. DJANGO VERSION CHECK
# ======================

$djangoVersion = Get-DjangoVersion
if ($djangoVersion -ne "Unknown") {
    $versionParts = $djangoVersion.Split('.')
    $majorVersion = [int]$versionParts[0]
    $minorVersion = [int]$versionParts[1]
    
    $isSupported = $true
    $message = "Django $djangoVersion"
    
    # Check LTS versions or recent versions
    if ($majorVersion -eq 4) {
        if ($minorVersion -lt 2) {
            $isSupported = $false
            $message = "Django $djangoVersion - Considera actualizar a 4.2+"
        }
    } elseif ($majorVersion -lt 4) {
        $isSupported = $false
        $message = "Django $djangoVersion - VERSION DESACTUALIZADA"
    }
    
    Add-Check -Description "Version de Django soportada" -Passed $isSupported -Weight 10 `
        -Message $message
} else {
    Add-Check -Description "Version de Django" -Passed $false -Weight 10 `
        -Message "No se pudo determinar la version"
}

# ======================
# 3. DEPENDENCY CHECKS
# ======================

Write-Host "ANALIZANDO DEPENDENCIAS..." -ForegroundColor Yellow

if (Test-Path $requirementsFile) {
    $content = Get-Content $requirementsFile
    
    # Check 9: Security packages
    $hasAxes = $content | Where-Object { $_ -match "^django-axes" }
    $hasCors = $content | Where-Object { $_ -match "^django-cors-headers" }
    
    $securityPackages = [bool]$hasAxes -bor [bool]$hasCors
    Add-Check -Description "Paquetes de seguridad instalados" -Passed $securityPackages -Weight 5 `
        -Message $(if ($securityPackages) {"Paquetes de seguridad presentes"} else {"Considera anadir django-axes o django-cors-headers"})
    
    # Check 10: Environment management
    $hasPythonDotenv = $content | Where-Object { $_ -match "^python-dotenv" }
    Add-Check -Description "Manejo de variables de entorno" -Passed $hasPythonDotenv -Weight 5 `
        -Message $(if ($hasPythonDotenv) {"python-dotenv instalado"} else {"python-dotenv recomendado"})
} else {
    Add-Check -Description "Archivo requirements.txt" -Passed $false -Weight 5 `
        -Message "Archivo requirements.txt no encontrado"
}

# ======================
# 4. DOCKER SECURITY CHECKS
# ======================

Write-Host "ANALIZANDO CONFIGURACION DOCKER..." -ForegroundColor Yellow

if (Test-Path $dockerComposeFile) {
    $dockerContent = Get-Content $dockerComposeFile -Raw
    
    # Check 11: Non-root user in Dockerfile
    $hasUserDirective = Test-FileContains -FilePath ".\Dockerfile" -Pattern "USER\s+\w+"
    Add-Check -Description "Usuario no-root en contenedor" -Passed $hasUserDirective -Weight 5 `
        -Message $(if ($hasUserDirective) {"Usuario no-root configurado"} else {"Considera usar usuario no-root"})
    
    # Check 12: Environment variables in docker-compose
    $hasEnvVars = $dockerContent -match "environment:"
    Add-Check -Description "Variables de entorno en docker-compose" -Passed $hasEnvVars -Weight 3 `
        -Message $(if ($hasEnvVars) {"Env vars configuradas"} else {"Env vars no configuradas"})
    
    # Check 13: Database password in docker-compose
    $dbPasswordExposed = $dockerContent -match "POSTGRES_PASSWORD.*['\"].*['\"]"
    Add-Check -Description "Passwords no hardcodeadas en docker-compose" -Passed (!$dbPasswordExposed) -Weight 4 `
        -Message $(if ($dbPasswordExposed) {"Passwords visibles en docker-compose"} else {"Passwords no visibles"})
} else {
    Add-Check -Description "Archivo docker-compose.yml" -Passed $false -Weight 5 `
        -Message "docker-compose.yml no encontrado"
}

# ======================
# 5. URL/ROUTING CHECKS
# ======================

Write-Host "ANALIZANDO RUTAS Y URLs..." -ForegroundColor Yellow

if (Test-Path $urlsFile) {
    # Check 14: Admin URL path
    $adminUrlStandard = Test-FileContains -FilePath $urlsFile -Pattern "admin/"
    Add-Check -Description "Admin URL no personalizada" -Passed $adminUrlStandard -Weight 3 `
        -Message $(if ($adminUrlStandard) {"Admin en ruta estandar"} else {"Admin en ruta personalizada (mejor seguridad)"})
}

# ======================
# RESULTS CALCULATION
# ======================

Write-Host ""
Write-Host "RESULTADOS DE SEGURIDAD" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host ""

# Display all checks
foreach ($check in $checks) {
    $status = if ($check.Passed) { "[PASS]" } else { "[FAIL]" }
    $color = if ($check.Passed) { "Green" } else { "Red" }
    
    Write-Host "$status $($check.Description)" -ForegroundColor $color
    Write-Host "   $($check.Message) (+$($check.Weight) puntos)" -ForegroundColor Gray
    Write-Host ""
}

# Calculate percentage and rating
$percentage = [math]::Round(($score / $maxScore) * 100)

if ($percentage -ge 85) {
    $rating = "EXCELENTE"
    $ratingColor = "Green"
} elseif ($percentage -ge 70) {
    $rating = "BUENA"
    $ratingColor = "Yellow"
} elseif ($percentage -ge 50) {
    $rating = "REGULAR"
    $ratingColor = "DarkYellow"
} else {
    $rating = "MALA"
    $ratingColor = "Red"
}

# Display final score
Write-Host "PUNTUACION FINAL" -ForegroundColor Magenta
Write-Host "==================" -ForegroundColor Magenta
Write-Host ""
Write-Host "Puntuacion: $score/$maxScore puntos" -ForegroundColor White
Write-Host "Porcentaje: $percentage%" -ForegroundColor White
Write-Host "Nivel de seguridad: $rating" -ForegroundColor $ratingColor

# Recommendations
Write-Host ""
Write-Host "RECOMENDACIONES" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan

$failedChecks = $checks | Where-Object { !$_.Passed }
if ($failedChecks.Count -gt 0) {
    Write-Host "Problemas encontrados:" -ForegroundColor Yellow
    foreach ($check in $failedChecks) {
        Write-Host "• $($check.Description): $($check.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "¡Excelente! Tu configuracion de seguridad es solida." -ForegroundColor Green
}

# Django version info
if ($djangoVersion -ne "Unknown") {
    Write-Host ""
    Write-Host "INFORMACION DJANGO" -ForegroundColor Gray
    Write-Host "   Version detectada: $djangoVersion"
    
    if ($majorVersion -lt 4) {
        Write-Host "   ATENCION: Django $djangoVersion ya no recibe actualizaciones de seguridad" -ForegroundColor Red
        Write-Host "   Recomendacion: Actualizar a Django 4.2 o superior" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Para analisis mas detallado:" -ForegroundColor Gray
Write-Host "   • Ejecuta: docker-compose exec web python manage.py check --deploy"
Write-Host "   • Revisa: https://docs.djangoproject.com/en/stable/topics/security/"
Write-Host ""

# Quick security test
Write-Host "TEST RAPIDO DE CONEXION" -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -Method Head -TimeoutSec 5 -ErrorAction SilentlyContinue
    if ($response) {
        Write-Host "Servidor Django accesible en http://localhost:8000" -ForegroundColor Green
    }
} catch {
    Write-Host "No se pudo conectar al servidor Django" -ForegroundColor Yellow
}
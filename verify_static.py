import os
import sys
from pathlib import Path

def verify_static_config():
    print("🔍 VERIFICANDO CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS")
    print("=" * 50)
    
    BASE_DIR = Path(__file__).resolve().parent
    errors = []
    warnings = []
    
    # 1. Verificar estructura de directorios
    print("\n📁 1. ESTRUCTURA DE DIRECTORIOS:")
    
    required_dirs = [
        BASE_DIR / 'src' / 'templates' / 'frontend' / 'assets',
        BASE_DIR / 'static',
        BASE_DIR / 'media',
        BASE_DIR / 'staticfiles',
    ]
    
    for dir_path in required_dirs:
        if dir_path.exists():
            print(f"   ✅ {dir_path.relative_to(BASE_DIR)}")
            # Contar archivos
            file_count = len(list(dir_path.rglob('*')))
            print(f"      📄 {file_count} archivos")
        else:
            print(f"   ❌ {dir_path.relative_to(BASE_DIR)} - NO EXISTE")
            errors.append(f"Directorio faltante: {dir_path.relative_to(BASE_DIR)}")
    
    # 2. Verificar archivos assets
    print("\n📄 2. ARCHIVOS ASSETS:")
    assets_dir = BASE_DIR / 'src' / 'templates' / 'frontend' / 'assets'
    
    if assets_dir.exists():
        file_types = {}
        for ext in ['.css', '.js', '.jpg', '.png', '.gif', '.svg', '.woff', '.woff2']:
            files = list(assets_dir.rglob(f'*{ext}'))
            if files:
                file_types[ext] = len(files)
        
        for ext, count in file_types.items():
            print(f"   📊 {ext}: {count} archivos")
    else:
        errors.append("Directorio de assets no encontrado")
    
    # 3. Verificar settings.py
    print("\n⚙️  3. CONFIGURACIÓN DJANGO:")
    settings_path = BASE_DIR / 'app' / 'project_settings' / 'settings.py'
    
    if settings_path.exists():
        with open(settings_path, 'r') as f:
            content = f.read()
        
        required_configs = [
            'STATIC_URL',
            'STATIC_ROOT', 
            'STATICFILES_DIRS',
            'MEDIA_URL',
            'MEDIA_ROOT'
        ]
        
        for config in required_configs:
            if config in content:
                print(f"   ✅ {config}")
            else:
                print(f"   ❌ {config} - NO ENCONTRADO")
                errors.append(f"Configuración faltante: {config}")
    else:
        errors.append("Archivo settings.py no encontrado")
    
    # 4. Verificar templates
    print("\n📄 4. VERIFICANDO TEMPLATES:")
    templates_dir = BASE_DIR / 'src' / 'templates'
    
    if templates_dir.exists():
        html_files = list(templates_dir.rglob('*.html'))
        print(f"   📊 {len(html_files)} archivos HTML encontrados")
        
        # Verificar un template de ejemplo
        if html_files:
            sample_file = html_files[0]
            with open(sample_file, 'r') as f:
                sample_content = f.read()
            
            if '{% load static %}' in sample_content:
                print(f"   ✅ Template tags cargados")
            else:
                warnings.append(f"Template sin {% load static %}: {sample_file.relative_to(BASE_DIR)}")
            
            # Verificar referencias estáticas
            import re
            static_refs = re.findall(r'src=["\']([^"\'>]*\.(css|js|jpg|png))["\']', sample_content)
            if static_refs:
                print(f"   📊 {len(static_refs)} referencias estáticas encontradas")
    else:
        errors.append("Directorio templates no encontrado")
    
    # Resumen
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE VERIFICACIÓN:")
    
    if errors:
        print("❌ ERRORES ENCONTRADOS:")
        for error in errors:
            print(f"   • {error}")
    else:
        print("✅ SIN ERRORES CRÍTICOS")
    
    if warnings:
        print("\n⚠️  ADVERTENCIAS:")
        for warning in warnings:
            print(f"   • {warning}")
    
    if not errors:
        print("\n🎉 ¡CONFIGURACIÓN CORRECTA!")
        print("\n🚀 Para probar:")
        print("   1. Ejecuta: python manage.py collectstatic")
        print("   2. Inicia el servidor: python manage.py runserver")
        print("   3. Visita: http://localhost:8000")
    else:
        print("\n🔧 Problemas por resolver antes de continuar")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = verify_static_config()
    sys.exit(0 if success else 1)

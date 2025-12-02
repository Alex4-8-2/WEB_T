import os
import sys
import django
from pathlib import Path

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings_temp')
django.setup()

from django.template.loader import get_template
from django.conf import settings

print("🔍 VERIFICACIÓN FINAL DE CONFIGURACIÓN")
print("=" * 50)
print(f"BASE_DIR: {settings.BASE_DIR}")
print(f"TEMPLATE DIRS: {settings.TEMPLATES[0]['DIRS']}")

# Verificar la ruta exacta
template_path = Path(r'D:\WEB_T\LOGIN\src\templates\frontend\index.html')
print(f"\n📄 Ruta REAL del template index.html: {template_path}")
print(f"¿Existe?: {'✅ SÍ' if template_path.exists() else '❌ NO'}")

# Verificar si Django puede encontrarlo
try:
    template = get_template('frontend/index.html')
    print("🎉 Django PUEDE encontrar el template!")
    print(f"Template encontrado: {template.origin.name}")
except Exception as e:
    print(f"❌ Error: {e}")
    
# Verificar rutas de búsqueda
print(f"\n🔎 Django buscará en estas rutas para 'frontend/index.html':")
from django.template.loaders.filesystem import Loader
loader = Loader(engine=django.template.engines['django'])
for template_dir in loader.get_dirs():
    test_path = Path(template_dir) / 'frontend' / 'index.html'
    print(f"  • {test_path} - {'✅ Existe' if test_path.exists() else '❌ No existe'}")

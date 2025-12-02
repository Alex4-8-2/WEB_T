# Script para correfer referencias estáticas en templates

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def fix_static_references():
    templates_dir = BASE_DIR / 'src' / 'templates'
    
    # Patrones para encontrar referencias a archivos estáticos
    patterns = [
        # CSS files
        (r'href=["\']([^"\'>]*\.css)["\']', r'href="{% static "\1" %}"'),
        # JS files
        (r'src=["\']([^"\'>]*\.js)["\']', r'src="{% static "\1" %}"'),
        # Images
        (r'src=["\']([^"\'>]*\.(jpg|jpeg|png|gif|svg|ico|webp))["\']', r'src="{% static "\1" %}"'),
        # Fonts
        (r'href=["\']([^"\'>]*\.(woff|woff2|ttf|eot))["\']', r'href="{% static "\1" %}"'),
    ]
    
    # Recorrer todos los archivos HTML
    for html_file in templates_dir.rglob("*.html"):
        print(f"Procesando: {html_file.relative_to(BASE_DIR)}")
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Añadir {% load static %} al inicio si no está
        if '{% load static %}' not in content and 'static' in content:
            # Buscar la etiqueta <html> o <head>
            if '<head>' in content:
                content = content.replace('<head>', '<head>\n    {% load static %}')
            elif '<html>' in content:
                content = content.replace('<html>', '<html>\n{% load static %}')
        
        # Reemplazar referencias estáticas
        for pattern, replacement in patterns:
            content = re.sub(pattern, replacement, content)
        
        # Guardar si hubo cambios
        if content != original_content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Corregido")
        else:
            print(f"  ℹ️  Sin cambios necesarios")

if __name__ == "__main__":
    fix_static_references()
    print("🎉 ¡Corrección completada!")

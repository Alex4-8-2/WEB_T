# admin_security.py
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.conf import settings

def superuser_required(view_func=None, login_url=None):
    """
    Decorador que requiere que el usuario sea superusuario.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

# Proteger todas las vistas de admin
def secure_admin_site(admin_site):
    """Aplica seguridad adicional al admin site"""
    for model, model_admin in admin_site._registry.items():
        # Hacer que todas las vistas requieran superusuario
        original_get_urls = model_admin.get_urls
        def get_urls_with_security(self):
            from django.urls import path
            from django.contrib.auth.views import LoginView
            from django.views.generic import RedirectView
            
            urls = original_get_urls()
            
            # Asegurar que todas las URLs requieran superusuario
            secure_urls = []
            for url in urls:
                if hasattr(url, 'callback'):
                    url.callback = superuser_required(url.callback)
                secure_urls.append(url)
            
            return secure_urls
        
        model_admin.get_urls = lambda self: get_urls_with_security(self)
    
    return admin_site

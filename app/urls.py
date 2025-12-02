from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API JWT Tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Páginas principales
    path('', TemplateView.as_view(template_name='frontend/index.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='frontend/login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='frontend/register.html'), name='register'),
    
    # API de usuarios (protegida con JWT)
    path('api/users/', include('core.urls')),
]

# Archivos estáticos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

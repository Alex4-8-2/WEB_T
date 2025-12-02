# api_views.py - Vistas para API de turismo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
def turismo_login(request):
    """API para login desde el frontend de turismo"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            password = data.get('password', '').strip()
            
            if not username or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Usuario y contraseña requeridos'
                }, status=400)
            
            # Autenticar con Django
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login exitoso',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Credenciales incorrectas'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Datos inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error del sistema: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def turismo_register(request):
    """API para registro desde el frontend de turismo"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            password2 = data.get('password2', '').strip()
            
            # Validaciones
            if not username or not email or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Todos los campos son requeridos'
                }, status=400)
            
            if password != password2:
                return JsonResponse({
                    'success': False,
                    'message': 'Las contraseñas no coinciden'
                }, status=400)
            
            if len(password) < 6:
                return JsonResponse({
                    'success': False,
                    'message': 'La contraseña debe tener al menos 6 caracteres'
                }, status=400)
            
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'El usuario ya existe'
                }, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'El email ya está registrado'
                }, status=400)
            
            # Crear usuario
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            user.save()
            
            # Auto-login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            
            return JsonResponse({
                'success': True,
                'message': 'Usuario registrado exitosamente',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error en el registro: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def turismo_logout(request):
    """API para logout"""
    if request.method == 'POST':
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Sesión cerrada'
        })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@csrf_exempt
def turismo_check(request):
    """API para verificar estado de sesión"""
    return JsonResponse({
        'authenticated': request.user.is_authenticated,
        'user': {
            'id': request.user.id if request.user.is_authenticated else None,
            'username': request.user.username if request.user.is_authenticated else None,
            'email': request.user.email if request.user.is_authenticated else None
        }
    })

@csrf_exempt
def turismo_sync(request):
    """API para sincronizar usuarios desde localStorage (solo para demo)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            users = data.get('users', [])
            action = data.get('action', '')
            
            # Solo registrar para demostración
            print(f"Sincronización recibida: {len(users)} usuarios, acción: {action}")
            
            return JsonResponse({
                'success': True,
                'message': f'Sincronización recibida ({len(users)} usuarios)',
                'count': len(users)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error en sincronización: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@login_required
def turismo_profile(request):
    """API para obtener perfil del usuario"""
    return JsonResponse({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'is_staff': request.user.is_staff,
        'last_login': request.user.last_login.isoformat() if request.user.last_login else None,
        'date_joined': request.user.date_joined.isoformat()
    })

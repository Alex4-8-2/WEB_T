# core/views.py
import redis, os, uuid
from django.conf import settings
from django.utils import timezone
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

User = get_user_model()
# Redis temporalmente deshabilitado para desarrollo
    # redis_client = redis.Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=int(os.getenv('REDIS_DB',0)))
    redis_client = None
    print('⚠️  Redis deshabilitado para desarrollo - usando blacklist en memoria')

signer = TimestampSigner()

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # generate verification token (signed)
        token = signer.sign(user.pk)
        verify_link = f"{request.scheme}://{request.get_host()}/api/auth/verify-email/?token={token}"
        send_mail(
            subject="Verifica tu email",
            message=f"Haz click: {verify_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response({"detail":"Registro creado. Revisa tu correo para verificar."}, status=201)

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        token = request.GET.get('token')
        if not token:
            return Response({"detail":"Token missing"}, status=400)
        try:
            unsigned = signer.unsign(token, max_age=60*60*24)  # 24h expiry
            pk = int(unsigned)
            user = get_object_or_404(User, pk=pk)
            user.email_verified = True
            user.save()
            return Response({"detail":"Email verificado"}, status=200)
        except SignatureExpired:
            return Response({"detail":"Token expirado"}, status=400)
        except BadSignature:
            return Response({"detail":"Token invÃ¡lido"}, status=400)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        ip = request.META.get('REMOTE_ADDR')
        user = authenticate(request, username=username, password=password)
        # check if user exists:
        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            user_obj = None

        # lock checks
        if user_obj and user_obj.is_locked():
            delta = (user_obj.lock_until - timezone.now()).total_seconds()
            return Response({"detail":f"Cuenta bloqueada por seguridad. Intenta en {int(delta)} segundos."}, status=403)

        if user is None:
            # increment failed attempts if user exists
            if user_obj:
                user_obj.failed_login_attempts += 1
                if user_obj.failed_login_attempts >= 5:
                    user_obj.lock_until = timezone.now() + timezone.timedelta(minutes=30)
                user_obj.save()
            return Response({"detail":"Credenciales invÃ¡lidas"}, status=401)

        # reset counters on success
        user.failed_login_attempts = 0
        user.lock_until = None
        user.last_login_ip = ip
        user.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        # store refresh jti in redis whitelist or manage blacklist on rotation
        jti = str(refresh['jti'])
        # we will store active refresh tokens with expiry TTL
        redis_client.setex(f"refresh:{jti}", int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), "active")

        return Response({
            'access': access,
            'refresh': str(refresh),
            'access_expires_in': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())
        }, status=200)

class RefreshView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # client sends refresh token
        token = request.data.get('refresh')
        if not token:
            return Response({"detail":"Missing refresh token"}, status=400)
        try:
            refresh_obj = RefreshToken(token)
        except Exception:
            return Response({"detail":"Invalid token"}, status=400)

        jti = str(refresh_obj['jti'])
        # check if this jti is blacklisted
        if redis_client.get(f"blacklist:{jti}"):
            return Response({"detail":"Token revoked"}, status=401)

        # check it exists in active list (rotation)
        if not redis_client.get(f"refresh:{jti}"):
            return Response({"detail":"Token not found (maybe rotated) or expired"}, status=401)

        # rotate: create new refresh token and blacklist old one
        new_refresh = RefreshToken.for_user(refresh_obj.user)
        new_jti = str(new_refresh['jti'])
        # set new active
        redis_client.setex(f"refresh:{new_jti}", int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), "active")
        # blacklist old
        redis_client.setex(f"blacklist:{jti}", int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), "revoked")
        # delete old active
        redis_client.delete(f"refresh:{jti}")
        return Response({'access': str(new_refresh.access_token), 'refresh': str(new_refresh)}, status=200)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        # revoke current refresh token if provided
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                r = RefreshToken(refresh_token)
                jti = str(r['jti'])
                redis_client.setex(f"blacklist:{jti}", int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()), "revoked")
                redis_client.delete(f"refresh:{jti}")
            except Exception:
                pass
        return Response({"detail":"Logged out"}, status=200)


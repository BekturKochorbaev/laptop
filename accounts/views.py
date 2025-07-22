import os

from django_rest_passwordreset.views import ResetPasswordRequestToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.viewsets import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, VerifyResetCodeSerializer
import requests
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.http import JsonResponse
from .models import UserProfile
from django.contrib.auth import login

class UserRegisterView(generics.CreateAPIView):
    """
    Регистрирует нового пользователя по email и паролю.
    """
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='refresh_token'),
            },
            required=['refresh_token']
        ),
    )
    def post(self, request):
        serializer = UserLogoutSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'detail': 'Вы успешно вышли.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import VerifyResetCodeSerializer


class VerifyResetCodeView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'reset_code', 'new_password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'reset_code': openapi.Schema(type=openapi.TYPE_INTEGER),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        )
    )
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# views.py


GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = "http://127.0.0.1:8000/accounts/api/auth/google/callback/" # или твой frontend uri


class GoogleAuthRedirectView(View):
    @swagger_auto_schema(
        operation_description="Redirects to Google OAuth2 login page",
        responses={
            302: openapi.Response("Redirects to Google OAuth2 authorization URL")
        }
    )
    def get(self, request):
        google_auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth"
            "?response_type=code"
            f"&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={GOOGLE_REDIRECT_URI}"
            "&scope=openid%20email%20profile"
            "&access_type=offline"
            "&prompt=consent"
        )
        return redirect(google_auth_url)


class GoogleAuthCallbackView(View):
    def get(self, request):
        code = request.GET.get("code")
        if not code:
            return JsonResponse({"error": "No code provided"}, status=400)

        # Получаем токен
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }
        token_response = requests.post(token_url, data=token_data)
        token_json = token_response.json()

        # Проверка на наличие ошибок в ответе Google
        if "error" in token_json:
            return JsonResponse({"error": token_json.get("error_description", "Token request failed")}, status=400)

        access_token = token_json.get("access_token")
        if not access_token:
            return JsonResponse({"error": "No access token received"}, status=400)

        # Получаем данные пользователя
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info = user_info_response.json()

        # Проверка на наличие ошибок в данных пользователя
        if "error" in user_info:
            return JsonResponse({"error": user_info.get("error_description", "User info request failed")}, status=400)

        # Извлекаем данные пользователя
        email = user_info.get("email")
        first_name = user_info.get("given_name", "")
        last_name = user_info.get("family_name", "")
        google_id = user_info.get("id")
        picture = user_info.get("picture", "")

        # Создаем или обновляем пользователя
        try:
            user, created = UserProfile.objects.get_or_create(
                email=email,
                defaults={
                    "username": email,  # Используем email как username
                    "first_name": first_name,
                    "last_name": last_name,
                }
            )
            if not created:
                # Обновляем данные существующего пользователя, если нужно
                user.first_name = first_name
                user.last_name = last_name
                user.save()

            # Аутентифицируем пользователя в Django
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        except Exception as e:
            return JsonResponse({"error": f"Failed to save user: {str(e)}"}, status=500)

        # Перенаправление на главную страницу
        return redirect("http://127.0.0.1:3000/")
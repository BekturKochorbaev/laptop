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


class UserRegisterView(generics.CreateAPIView): # Регистрация для обычных пользователей
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


@api_view(['POST'])
def verify_reset_code(request):
    serializer = VerifyResetCodeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Пароль успешно сброшен.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='email'),
        },
        required=['refresh_token']
    ),
)
def custom_password_reset(request):
    response = ResetPasswordRequestToken.as_view()(request._request)
    if response.status_code == 200:
        return Response({'status': "Код отправлен"}, status=status.HTTP_200_OK)
    return response

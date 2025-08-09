from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.viewsets import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer, VerifyResetCodeSerializer, UserGetSerializers
from .models import UserProfile
from rest_framework.response import Response
from rest_framework import status


class UserGetApiView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserGetSerializers

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


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



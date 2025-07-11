from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from datetime import datetime
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer): # Регистрация для обычных пользователей
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = UserProfile(**validated_data)
        user.set_password(password)  # <-- хеширует пароль
        user.save()
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        access_token_expiration = datetime.fromtimestamp(refresh.access_token['exp']).isoformat()
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'access_token_expiration': access_token_expiration,
        }


class UserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get('refresh_token')
        if not refresh_token:
            raise serializers.ValidationError('Refresh токен не предоставлен.')
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError as e:
            raise serializers.ValidationError('Недействительный токен.')

        return attrs


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()  # Email пользователя
    reset_code = serializers.IntegerField()  # 4-значный код
    new_password = serializers.CharField(write_only=True)  # Новый пароль

    def validate(self, data):
        email = data.get('email')
        reset_code = data.get('reset_code')

        # Проверяем, существует ли указанный код для email
        try:
            token = ResetPasswordToken.objects.get(user__email=email, key=reset_code)
        except ResetPasswordToken.DoesNotExist:
            raise serializers.ValidationError("Неверный код сброса или email.")

        data['user'] = token.user
        return data

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']

        # Устанавливаем новый пароль
        user.set_password(new_password)
        user.save()
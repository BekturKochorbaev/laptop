from .views import (UserRegisterView, UserLoginView, UserLogoutView,
                    verify_reset_code, custom_password_reset)
from django.urls import path

urlpatterns = [

    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
    path('password_reset/', custom_password_reset, name='custom_password_reset'),

]
from .views import (UserRegisterView, UserLoginView, UserLogoutView,
                    VerifyResetCodeView, UserGetApiView)
from django.urls import path, include


urlpatterns = [

    path('user-me/', UserGetApiView.as_view(),name='user-me'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('password_reset/verify_code/', VerifyResetCodeView.as_view(), name='verify_reset_code'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]


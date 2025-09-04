from django.contrib import admin
from django.contrib.auth.models import Group
from django_rest_passwordreset.models import ResetPasswordToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from .models import UserProfile


admin.site.register(UserProfile)
admin.site.unregister(Group)
admin.site.unregister(ResetPasswordToken)
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)
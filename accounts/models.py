from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(region=None, null=True, blank=True)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


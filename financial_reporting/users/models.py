from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', null=True, blank=True)

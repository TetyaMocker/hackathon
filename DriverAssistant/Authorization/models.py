from django.db import models
from django.contrib.auth.models import User


class UserFlag(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return f'Пользователь: {self.user.username}'

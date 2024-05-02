from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class AccountSystem(AbstractUser):
    phone_number = models.TextField(null=True, blank=True)

    class Meta(AbstractUser.Meta):
        db_table = '老师账号表'
        verbose_name = '管理员和老师账号表'
        verbose_name_plural = '管理员和老师账号表'

    def __str__(self):
        verbose_name = self.username + ' '
        if self.is_superuser:
            verbose_name += '管理员'
        else:
            verbose_name += '老师'
        return verbose_name


from django.db import models

# Create your models here.
class Users(models.Model):
    login = models.CharField('login', max_length=32)
    password = models.CharField('password', max_length=32)
    key = models.CharField('key', max_length=32)
    authorization = models.BooleanField('authorization')

    def __str__(self):
        return self.login

import os
import logging
from django.db import models
from users.models import Users

# Create your models here.
class Analyse(models.Model):
    user_key = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='analyses')
    image = models.ImageField(upload_to='images/', verbose_name='image')
    datetime = models.CharField('date', max_length=128, default="27-11-2024 00:00:00")
    model_1 = models.CharField('model 1', max_length=8)
    model_2 = models.CharField('model 2', max_length=8)
    model_3 = models.CharField('model 3', max_length=8)
    ensemble = models.CharField('result', max_length=8)

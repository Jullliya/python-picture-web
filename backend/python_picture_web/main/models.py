from django.db import models

# Create your models here.
class Analyse(models.Model):
    image = models.ImageField()
    model_1 = models.CharField('model 1', max_length=8)
    model_2 = models.CharField('model 2', max_length=8)
    model_3 = models.CharField('model 3', max_length=8)
    ensemble = models.CharField('result', max_length=8)
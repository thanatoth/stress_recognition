from django.db import models

from django.db import models
import numpy as np
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length = 128)
    image = models.ImageField(upload_to='faces', default = None, null = True, blank = True)
    predicted = models.IntegerField(default = None, null = True, blank = True)

    def __str__(self):
        return self.name

class UserCondition(models.Model):


    user_name = models.CharField(max_length = 128, default = None, null = True, blank = True)
    #user_name = models.ForeignKey(User, on_delete=models.CASCADE) # 1対多対応
    expression = models.CharField(max_length = 128)
    weather = models.CharField(max_length = 128)
    temp_max = models.FloatField()
    temp_min = models.FloatField()
    diff_tmp = models.FloatField()
    humidity = models.FloatField()
    predicted = models.IntegerField(default = None, null = True, blank = True)

class Photo(models.Model):
    image = models.ImageField(upload_to='faces')
    pub_date = models.DateTimeField(verbose_name='date_published', default = None, null = True, blank = True)


class Model(models.Model):
    name = models.CharField(max_length=100)
    predicted = models.CharField(max_length = 128)

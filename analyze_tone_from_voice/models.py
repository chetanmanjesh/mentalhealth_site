from django.db import models

# Create your models here.

# Create Model for Depression
class Depression(models.Model):
    index = models.IntegerField()
    link = models.CharField(max_length = 500)

# Create Model for Stress
class Stress(models.Model):
    index = models.IntegerField()
    link = models.CharField(max_length = 500)

class Person2(models.Model):
    location =  models.CharField(max_length = 500)
    url = models.CharField(max_length = 500)
    age = models.CharField(max_length = 500)
    gender = models.CharField(max_length = 500)
    comments = models.CharField(max_length=500)
    disorder = models.CharField(max_length=500)


from django.db import models


# Create your models here.
class User_data(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    count=models.IntegerField(default=0)


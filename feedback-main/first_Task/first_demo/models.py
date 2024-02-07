from django.db import models

# Create your models here.
class feedback_model(models.Model):
    name = models.CharField(max_length=100)
    feedback = models.TextField(max_length=1000)
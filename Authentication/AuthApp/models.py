from django.db import models


# Create your models here.
class User_data(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    count=models.IntegerField(default=0)

    
# class Module(models.Model):
#     product_name=models.CharField(max_length=100)
#     customer_name=models.CharField(max_length=100)
#     phone_no=models.CharField(max_length=100)
#     price=models.CharField(max_length=100)
#     waranty=models.CharField(max_length=100)
#     product_id=models.CharField(max_length=100)
#     product_details=models.CharField(max_length=1000)


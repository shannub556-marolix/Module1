from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User_data #Module#Product

class userseralizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','email']



class user_data_seralizer(serializers.ModelSerializer):
    class Meta:
        model=User_data
        fields='__all__'

# class Module_seralizer(serializers.ModelSerializer):
#     class Meta:
#         model=Module
#         fields='__all__'


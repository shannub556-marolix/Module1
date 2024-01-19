from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User_data

class userseralizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','password','email']



class user_data_seralizer(serializers.ModelSerializer):
    class Meta:
        model=User_data
        fields='__all__'
from rest_framework import serializers
from .models import *

class feedback_serializer(serializers.ModelSerializer):
 class Meta:
       model = feedback_model
       fields = "__all__"
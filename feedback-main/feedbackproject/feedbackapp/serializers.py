from rest_framework import serializers
from .models import feedbacktables


class feedback_serializer(serializers.ModelSerializer):
    class Meta:
        model = feedbacktables
        fields = "__all__"
from django.shortcuts import render
from django.http import HttpResponse
from .models import * 
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['GET'])
def feedbacklist(request):
    # return HttpResponse("Hello World")
    feedback_obj = feedbacktables.objects.all()
    serializer = feedback_serializer(feedback_obj, many=True)
    return Response(serializer.data)


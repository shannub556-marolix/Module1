from django.shortcuts import render

# Create your views here.
from .serializer import userseralizer
from django.contrib.auth.models import User
from rest_framework.response import Response
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(["POST","GET"])
def input(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']
        user_details=User(username=username,password=password,email=email)
        user_details.save()    
        return Response({"Key":"valuye"},status=status.HTTP_202_ACCEPTED)
    return JsonResponse('Succesfull',safe=False)

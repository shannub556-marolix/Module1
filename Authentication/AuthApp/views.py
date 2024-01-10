from django.shortcuts import render

# Create your views here.
from .serializer import userseralizer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["POST"])                      #csrf token will be verification will be done here 
def input(request):
    if request.method=='POST' :
        username=request.data['username']
        password=request.data['password']
        email=request.data['email']
        user_details=User.objects.create_user(username=username,password=password,email=email)  #Saving the user
        user_details.save()
    serilizer=userseralizer(user_details)    #converting the user details using serilizer
    return Response(serilizer.data)          #returning the data

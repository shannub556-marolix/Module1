from django.shortcuts import render
from rest_framework import status

# Create your views here.
from .serializer import userseralizer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate

@api_view(["POST"])                      #csrf token will be verification will be done here 
def input(request):
    if request.method=='POST' :
        username=request.data['username']
        password=request.data['password']
        email=request.data['email']
        try:
            user_details=User.objects.create_user(username=username,password=password,email=email)  #Saving the user
            user_details.save()
        except:
            return Response({"Message" : "username already exsists try again "})         # if username already exsists
    serilizer=userseralizer(user_details)    #converting the user details using serilizer
    return Response(serilizer.data)          #returning the data


@api_view(["POST"])
def login(request):
    if request.method=="POST":
        username=request.data['username']
        password=request.data['password']
        user_details=authenticate(username=username,password=password)     #if user is not valid it will return None
        if user_details is not None:
            return Response({'message': 'Valid user'})
    return Response({'message':'Invalid User'})


@api_view(["PUT"])
def reset(request):
    if request.method=="PUT":
        username=request.data['username']
        New_password=request.data['password']
        email=request.data['email']
        try:
            user_details=User.objects.get(username=username)
            seralizer=userseralizer(user_details)
            if email==seralizer.data['email']:
                updateduser_details,value=User.objects.update_or_create(username=username,email=email,defaults={"password":New_password})    #inbulit method to update password 
                return Response({'message': f"{updateduser_details} user password reset reset succesful with ({New_password}) "})            # click here to know about syntax  https://stackoverflow.com/questions/16329946/django-model-method-create-or-update
        except:
            return Response({'message':"user not found "})
    return Response(status=status.HTTP_200_OK)

        




from django.shortcuts import render
from rest_framework import status
from .serializer import userseralizer,user_data_seralizer,Module_seralizer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from django.contrib.auth.hashers import check_password
from .models import User_data


@api_view(["POST"])                      #csrf token will be verification will be done here 
def input(request):
    if request.method=='POST':
        username=request.data['username']
        password=request.data['password']
        email=request.data['email']
        try:
            user_details=User.objects.create_user(username=username,password=password,email=email)  #Saving the user
            user_details.save()
            token=Token.objects.create(user=user_details)
            serilizer1=user_data_seralizer(data=request.data)
            if serilizer1.is_valid():
                serilizer1.save()
        except:
            return Response({"Message" : "username already exsists try again "})         # if username already exsists
        serilizer=userseralizer(user_details)    #converting the user details using serilizer
        return Response({'token':token.key, "user": serilizer.data})          #returning the data


@api_view(["POST"])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,TokenAuthentication])
def login(request):
    if request.method=="POST":
        username=request.data['username']
        password=request.data['password']
        user_details=authenticate(username=username,password=password)     #if user is not valid it will return None
        if user_details is not None:
            user_details=User.objects.get(username=username)
            token,value=Token.objects.get_or_create(user=user_details)
            serializer=userseralizer(user_details)
            user_data=User_data.objects.get(username=username)
            serializer1=user_data_seralizer(user_data)
            count=serializer1.data['count']
            count=int(count)+1
            User_data.objects.filter(username=username).update(count=count)
            return Response({'message': 'Valid user','token':token.key,'user':serializer.data})
    return Response({'message':'Invalid User'})

@api_view(["PUT"])
def reset(request):
    if request.method == "PUT":
        username = request.data.get('username')
        new_password = request.data.get('password')  
        email = request.data.get('email')
        if not all([username, new_password, email]):
            return Response({'message': "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_details = User.objects.get(username=username)
            serializer = userseralizer(user_details)
            if email == serializer.data['email']:
                #user, created = User.objects.update_or_create(username=username, email=email,defaults={'password': new_password})          # this method will automatically replace and save paticular feild , but it won't encript password
                user=User.objects.get(username=username)
                user.set_password(new_password)                                                    #set_password is inbulit method which will encrpt new password 
                user.save()                                                                        #it will save encrypted password
                return Response({'message': "User updated"})                                                                                   
            else:
                return Response({'message': "Email does not match."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': "User not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(status=status.HTTP_200_OK)


#Venkat's code  

@api_view(["PUT"])
def change_password(request):
    if request.method == "PUT":
        current_password = request.data['current_password']
        new_password = request.data['new_password']
        username = request.data['username']
        if not all([current_password, new_password,username]):
            return Response({'message': "Both current and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_details = User.objects.get(username=username)
            if check_password(current_password,user_details.password):
                #user, created = User.objects.update_or_create(username=username, defaults={'password': new_password})                  # this method will automatically replace and save paticular feild , but it won't encript password
                user=User.objects.get(username=username)
                user.set_password(new_password)                                    #set_password is inbulit method which will encrpt new password 
                user.save()                                                        #it will save encrypted password
                return Response({'message': "Password changed successfully"})
            return Response({"message": "current password is incorrect"})
        except:
            return Response({'message': "User with that details not found."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def visitors(request):
    visitors_count=0
    data=User_data.objects.all()
    serilizer=user_data_seralizer(data,many=True)
    for value in serilizer.data:
        visitors_count+=value['count']
    return Response({"Visitors count":visitors_count})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response({"Note" : "Authorization was Succesful and token deleted ",
        "message": "logout was successful"})

@api_view(['POST'])
def module(request):
    serilizer1=Module_seralizer(data=request.data)
    if serilizer1.is_valid():
        serilizer1.save()
    return Response(serilizer1.data)



from django.shortcuts import render
from rest_framework import status
import secrets
# Create your views here.
from .serializer import userseralizer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .serializer import ForgotPasswordSerializer
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication,TokenAuthentication


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
        except:
            return Response({"Message" : "username already exsists try again "})         # if username already exsists
        serilizer=userseralizer(user_details)    #converting the user details using serilizer
        #data={'token':token.key, "user": serilizer.data}
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
            token=Token.objects.get(user=user_details)
            serializer=userseralizer(user_details)
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
                # Using update_or_create
                user, created = User.objects.update_or_create(username=username, defaults={'password': new_password, 'email': email})
                # If you want to save after updating, which is not necessary here since the above method saves automatically.
                # user.save()
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
        current_password = request.data.get('current_password')
        new_password = request.data.get('newpassword')
        
        if not all([current_password, new_password]):
            return Response({'message': "Both current and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        if user.check_password(current_password):
            if current_password == new_password:
                return Response({'message':"new password must be different from old password"},status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message': "Password changed successfully"})
        else:
            return Response({'message': "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_200_OK)

@api_view(["POST"])
def forgot_password(request):
    if request.method == "POST":
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        
        # Fetch the user associated with the email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': "No user found with the provided email."}, status=status.HTTP_404_NOT_FOUND)
        
        # Generate a unique reset token
        reset_token = secrets.token_hex(16)

        # Generate and send a reset link/token to the user's email
        # Note: You'd typically create a token or a reset link and include it in the email.
        # For demonstration purposes, here's a simple email sending code:
        reset_link = f"http://yourdomain.com/reset_password/{reset_token}/"

        send_mail('Password Reset',f'Please click on the following link to reset your password: {reset_link}',
              'from@example.com',[user.email],fail_silently=False,
              )

        return Response({'message': "Password reset email sent."}, status=status.HTTP_200_OK)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserProfileSerializer, UserRegistrationSerializer, SoldProductsSerializer
from django.contrib.auth import authenticate
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User,SoldProducts

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

class UserRegistrationView(APIView):
  renderer_classes = [UserRenderer]    #why render classes
  def post(self, request, format=None):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = get_tokens_for_user(user)
    return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    password = serializer.data.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
      token = get_tokens_for_user(user)
      return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
    else:
      return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
    
class CreateSuperUser(APIView):
  renderer_classes=[UserRenderer]
  def post(self,request, format=None):
    email=request.data['email']
    password=request.data['password']
    user = authenticate(email=email, password=password)
    if user is not None:
      user_data=User.objects.get(email=email)
      if user_data.is_admin:
        email1=request.data['email1']
        password1=request.data['password1']
        tc=request.data['tc']
        name1=request.data['name1']
        superuser=User.objects.create_superuser(name=name1,email=email1,password=password1,tc=tc)
        superuser.save()
        token = get_tokens_for_user(superuser)
        return Response({'token':token, 'msg':'Super User Registration Successful'}, status=status.HTTP_201_CREATED)
      else:
        return Response('Unauthorized user , Access denied',status=status.HTTP_401_UNAUTHORIZED)
    return Response({'errors':{'non_field_errors':['name or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)



class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)
  

class SoldProducts_details(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    name=serializer.data['name']
    email=serializer.data['email']
    mobile=request.data['mobile']
    product_code=request.data['product_code']
    product_name=request.data['product_name']
    product_expiry=request.data['product_expiry']
    product_mfd=request.data['product_mfd']
    product_waranty=request.data['product_waranty']
    product_category=request.data['product_category']
    details=SoldProducts(name=name,email=email,mobile=mobile,product_code=product_code,product_name=product_name,product_expiry=product_expiry,product_mfd=product_mfd,product_waranty=product_waranty,product_category=product_category)
    details.save()
    product_data=SoldProducts.objects.get(product_code=product_code)
    serializer=SoldProductsSerializer(product_data)
    return Response(serializer.data,status=status.HTTP_200_OK)
  
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    email=serializer.data['email']
    details=SoldProducts.objects.filter(email=email)
    serializer=SoldProductsSerializer(details,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)
  

class AllSoldProducts(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    email=serializer.data['email']
    user=User.objects.get(email=email)
    if user.is_admin:
      details=SoldProducts.objects.all()
      serializer=SoldProductsSerializer(details,many=True)
      return Response(serializer.data,status=status.HTTP_200_OK)
    return Response('Unauthorized user',status=status.HTTP_202_ACCEPTED)


    

class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
  

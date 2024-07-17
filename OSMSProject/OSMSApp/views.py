

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import RegistrationSerializer, LoginSerializer, ProfileSerializer , LogoutSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse,HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from .password_reset_file import reset_password 
from .send_otp_logic import sendOtp
from .renderers import UserRenderer
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect,reverse
from .Sms import Message
import jwt


SECRET_KEY = 'django-insecure-)x(whe5a#q(pm@^oyz-7m9h#%dpwjo7_ds5qfkeh1-ns@mb@gw'

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def decode_access_token(token):
    payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
    return payload['user_id']


class Home(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        return render(request,'Home.html')

# Create your views here.
class userregistration(APIView):
    renderer_classes = [UserRenderer]
    #template_name = 'templates/Home.html'
    def get(self, request, format=None):
        return render(request,'signup.html')
    def post(self, request, formate=None):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                Tokens=get_tokens_for_user(user)
                try:
                    Message.send(f'Hello {serializer.data['name']}, You have Succesfully Created your Account with EMail id - {serializer.data['email']}')
                except:
                    pass
                return HttpResponseRedirect('login/')
            return render(request,'signup1.html')
        except:
            return render(request,'signup1.html')
        
    
    
class userlogin(APIView):
    renderer_classes = [UserRenderer]
    #template_name = 'templates/Home.html'
    def get(self, request, format=None):
        if 'auth' in request.COOKIES:
            return redirect('viewprofile')
        return render(request,'login.html')
    def post(self, request, formate=None):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                email = serializer.data.get('email')
                password = serializer.data.get('password')
                user = authenticate(email = email, password=password)
                if user is not None:
                    user = User.objects.get(email = email)
                    Tokens=get_tokens_for_user(user)
                    response= HttpResponseRedirect('profile/')
                    response.set_cookie('auth',Tokens['access'])
                    return response
                else:
                    return render(request, 'login1.html')
            return render(request, 'login1.html')     
        except:
            return render(request, 'login1.html')
        
class userlogin2(userlogin):
    def get(self, request, format=None):
        if 'auth' in request.COOKIES:
            return redirect('viewprofile')
        return render(request,'profile2.html')


    
class profileview(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        if 'auth' in request.COOKIES:
            access=request.COOKIES['auth']
        try:
            id=decode_access_token(access)
            user = User.objects.get(id=id)
            serializer=ProfileSerializer(user)
            data={"id":serializer.data['id'],"name":serializer.data['name'],"email":serializer.data['email']}
        except:
            return redirect('login1')
        return render(request,'profile.html',data)
    def post(self, request, format=None):
        response = redirect('login')
        response.delete_cookie('auth')
        return response
        
    
class userlogout(APIView):       #here we have to pass access token 
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

 
class Forget(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        return render(request,'forget.html')
    def post(self,request):
        email = request.data['email']
        resp = sendOtp(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email = email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'check-pass/'+uid+'/'+token+'/'
            print('Password Reset Link', link)
            Tokens=get_tokens_for_user(user)
            return HttpResponseRedirect(link)
        return render(request, 'forget1.html')
    
class Forget1(Forget):
    def get(self, request, format=None):
        return render(request,'check1.html')


class Checkpass(APIView):
    renderer_classes = [UserRenderer]
    #template_name = 'templates/Home.html'
    def get(self, request, uid, token, format=None):
        try:
            self.uid = uid
            self.token = token
            id = smart_str(urlsafe_base64_decode(uid))
            Checkpass.user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(Checkpass.user, token):
                return redirect('forget1')
            #return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)
            return render(request,'check.html')
        except DjangoUnicodeDecodeError as identifier:
            return redirect('forget1')
    def post(self, request,  uid, token, formate=None):
        otp = request.data.get('otp')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        user=Checkpass.user
        serializer=ProfileSerializer(user)
        email=serializer.data['email']
        cached_otp = cache.get(email)
        if cached_otp is None or cached_otp != otp:
            return redirect('forget1')
        if password != password2:
            return  redirect('forget1')
        user.set_password(password)
        user.save()
        cache.delete(email)
        return redirect('login')






@api_view(['POST'])
def confirm_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    
    cached_otp = cache.get(email)
    if cached_otp is None or cached_otp != otp:
        return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')

    result = reset_password(email, password, confirm_password)  
    return result 

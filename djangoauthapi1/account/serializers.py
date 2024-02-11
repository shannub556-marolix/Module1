
from rest_framework import serializers
from account.models import User,SoldProducts as SoldProduct
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from account.utils import Util
from random import randint
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registration Request
  password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'password', 'password2', 'tc']
    extra_kwargs={
      'password':{'write_only':True}
    }

  # Validating Password and Confirm Password while Registration
  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")    # will it take control out of this class
    return attrs

  def create(self, validate_data):
    return User.objects.create_user(**validate_data)

class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name']

class SoldProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = SoldProduct
    fields = ['product_code','email', 'name','mobile','product_name','product_expiry','product_mfd','product_waranty','product_category','date']

class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')         #we are getting it by token??
    if password != password2:
      raise serializers.ValidationError("Password and Confirm Password doesn't match")
    user.set_password(password)
    user.save()
    return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/reset-password/'+uid+'/'+token
      print('Password Reset Link', link)
      otp=randint(1000,9999)
      User.objects.filter(email=email).update(otp=otp)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link+f' and otp to reset your password is {otp}'
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')
    

class OtpSeralizer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields=['otp']

class UserPasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  otp = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password', 'password2','otp']

  def validate(self, attrs):
    try:
      password = attrs.get('password')
      password2 = attrs.get('password2')
      otp=attrs.get('otp')
      uid = self.context.get('uid')
      token = self.context.get('token')
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      serializer=OtpSeralizer(user)
      print(serializer.data)
      if otp!=serializer.data['otp']:
        return serializers.ValidationError("Wrong otp please try again")
      if password != password2:
        raise serializers.ValidationError("Password and Confirm Password doesn't match")
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
    

class ResetpasswordSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    if User.objects.filter(email=email).exists():
      user = User.objects.get(email = email)
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/verifyotp/'+uid+'/'+token
      print('Password Reset Link', link)
      otp=randint(1000,9999)
      User.objects.filter(email=email).update(otp=otp)
      # Send EMail
      body = 'Click Following Link to Reset Your Password '+link+f' and otp to reset your password is {otp}'
      data = {
        'subject':'Reset Your Password',
        'body':body,
        'to_email':user.email
      }
      Util.send_email(data)
      attrs['link']=body
      return attrs
    else:
      raise serializers.ValidationError('You are not a Registered User')
    

class VerifyotpSerializer(serializers.Serializer):
  otp = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['otp']

  def validate(self, attrs):
    try:
      otp=attrs.get('otp')
      uid = self.context.get('uid')
      token = self.context.get('token')
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      serializer=OtpSeralizer(user)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      if otp!=serializer.data['otp']:
        raise serializers.ValidationError("Wrong otp please try again")
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded UID', uid)
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password Reset Token', token)
      link = 'http://localhost:8000/setpassword/'+uid+'/'+token
      print('Password Reset Link', link)
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
    

class SetpasswordSerializer(serializers.Serializer):
  password1 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
  class Meta:
    fields = ['password1','password2']

  def validate(self, attrs):
    try:
      password1=attrs.get('password1')
      password2=attrs.get('password2')
      uid = self.context.get('uid')
      token = self.context.get('token')
      id = smart_str(urlsafe_base64_decode(uid))
      user = User.objects.get(id=id)
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not Valid or Expired')
      if password1!=password2:
        raise serializers.ValidationError('password1 and password doesnt matches please try again')
      user.set_password(password1)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError as identifier:
      PasswordResetTokenGenerator().check_token(user, token)
      raise serializers.ValidationError('Token is not Valid or Expired')
    
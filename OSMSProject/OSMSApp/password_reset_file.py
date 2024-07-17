from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import User

def reset_password(email, password, confirm_password):
    if password != confirm_password:
        return Response({"message": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)
    
    cached_otp = cache.get(email)
    if cached_otp is None:
        return Response({"message": "OTP expired or not requested"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
    
    user.set_password(password)
    user.save()
    
    cache.delete(email)
    
    subject = 'Password changed'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    # HTML email content
    html_message = render_to_string('password_reset_email.html', {'password': password})
    
    try:
        email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
        email.attach_alternative(html_message, 'text/html')
        email.send()
        return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
    except:
        return Response({"message": "Password reset successful, but failed to send notification mail due to timeout"}, status=status.HTTP_408_REQUEST_TIMEOUT)
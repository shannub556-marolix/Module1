from django.core.cache import cache
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from django.utils.crypto import get_random_string
from .models import User

def sendOtp(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({"message": "User not found with this email"}, status=status.HTTP_404_NOT_FOUND)
    
    otp = get_random_string(length=4, allowed_chars='1234567890')
    cache.set(email, otp, timeout=300)
    
    subject = 'Password Reset OTP'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    # HTML email content
    html_message = render_to_string('send_otp_email.html', {'otp': otp})
    
    try:
        email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
        email.attach_alternative(html_message, 'text/html')
        email.send()
        return JsonResponse({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
    except:
        return JsonResponse({"message": "Failed to send OTP"}, status=status.HTTP_408_REQUEST_TIMEOUT)


   
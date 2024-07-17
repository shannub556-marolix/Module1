from django.urls import path
from .views import *
urlpatterns = [
    path('', Home.as_view(), name="Home"),
    path('registration/', userregistration.as_view(), name="registration"),
    path('registration/login/', userlogin.as_view(), name="login"),
    path('registration/login1/', userlogin2.as_view(), name="login1"),
    path('forget/', Forget.as_view(), name="forget"),
    path('forget1/', Forget1.as_view(), name="forget1"),
    path('logout/', userlogout.as_view(), name="logout"),
    path('registration/login/profile/', profileview.as_view(), name="viewprofile"),
    path('registration/login1/profile/', profileview.as_view(), name="viewprofile"),
    path('forget/check-pass/<uid>/<token>/', Checkpass.as_view(), name="Checkpass"),
    path('forget1/check-pass/<uid>/<token>/', Checkpass.as_view(), name="Checkpass"),
    
    #path('send_otp/',send_otp,name="sendOtp"),
    path('confirm_otp/',confirm_otp,name="confirmotp"),
    path('reset_password/',reset_password_view,name="reset_password"),



]
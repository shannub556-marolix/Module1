
from django.urls import path
from account.views import  UserPasswordResetView,UserLoginView, UserProfileView, UserRegistrationView, UserChangePasswordView,SendPasswordResetEmailView,CreateSuperUser,SoldProducts_details,AllSoldProducts, Verifyotp,Setpassword,Resetpassword
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('sendresetpasswordemail/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    path('create-superuser',CreateSuperUser.as_view(),name='create-superuser'),
    path('sold-products',SoldProducts_details.as_view(),name='Sold-Products'),
    path('allsold-products',AllSoldProducts.as_view(),name='AllSold-Products'),
    path('resetuserpassword', Resetpassword.as_view(), name='reset-password'),
    path('verifyotp/<uid>/<token>/',Verifyotp.as_view(),name='Verify-otp'),
    path('setpassword/<uid>/<token>/',Setpassword.as_view(),name='Set-password'),

    # path('passwordchange/',auth_views.PasswordChangeView.as_view(),name='passwordchange'),
    # path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(),name='passwordresetchange'),
    path('resetpassword/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='resetpassword'),
    # path('passwordresetcomplete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetcomplete.html'),name='passwordresetcomplete')

]
from django.urls import path
from .views import feedbacklist
urlpatterns = [
    path('',feedbacklist),
   
]
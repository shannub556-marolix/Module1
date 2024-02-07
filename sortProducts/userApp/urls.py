from django.urls import path
from .views import ProductList, FeedbackList

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('feedback/', FeedbackList.as_view(), name='feedback-list'),
]
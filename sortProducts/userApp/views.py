from rest_framework import generics
from .models import Product, Feedback
from .serializers import ProductSerializer, FeedbackSerializer
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends=(DjangoFilterBackend,SearchFilter,OrderingFilter)
    filterset_fields=['category']
    search_fields=('product_name','price','category')
    ordering_fields=('product_name','price','id')


class FeedbackList(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

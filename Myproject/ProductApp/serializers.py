from rest_framework import serializers
from.models import Product,ProductDiscount,Bestseller


class Productserializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductDiscount
        fields=['id','prodname','pdiscount']

class Bestsellerserializer(serializers.ModelSerializer):
    class Meta:
        model=Bestseller
        fields='__all__'

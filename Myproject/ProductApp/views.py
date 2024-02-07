from django.shortcuts import render
from.models import Product,ProductDiscount,Bestseller
from.serializers import Productserializer,DiscountSerializer,Bestsellerserializer
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET','POST'])
def Product_data(request):
    if request.method=='GET':
        prod=Product.objects.all()
        serializer=Productserializer(prod,many=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED,safe=False)
    elif request.method=='POST':
        serializer=Productserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        org_price=serializer.data['original_price']
        new_price=serializer.data['new_price']
        dis_price=int(org_price)-int(new_price)
        dis_per=(dis_price/int(org_price))*100
        dis_per=str(dis_per)+'%'
        Product.objects.filter(pcode=serializer.data['pcode']).update(discount_per=dis_per)
        serializer1=Product.objects.get(pcode=serializer.data['pcode'])
        serializer1=Productserializer(serializer1)
    return Response(serializer1.data,status=status.HTTP_201_CREATED)
    #return Response(status=status.HTTP_102_PROCESSING)


@api_view(['GET','PUT','DELETE'])
def Product_details(request,id):
    try:
        prod=Product.objects.get(pk=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method=='GET':
        serializer=Productserializer(prod)
        count=serializer.data['prod_count']
        count=int(count)+1
        Product.objects.filter(pk=id).update(prod_count=count)
        return JsonResponse(serializer.data)
    elif request.method=='PUT':
        serializer=Productserializer(prod,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method=='DELETE':
        prod.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_102_PROCESSING)

@api_view(['POST','GET','PUT','DELETE'])
def product_discount(request):
    if request.method=='POST':
        serializer=DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    #return Response(status=status.HTTP_201_CREATED)

    elif request.method=='GET':
        discount_products=ProductDiscount.objects.all()
        serializer =DiscountSerializer(discount_products,many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method=='PUT':
        discount_products = ProductDiscount.objects.get(prodname=request.data['prodname'])
        serializer=DiscountSerializer(discount_products,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    elif request.method=='DELETE':
        discount_products = ProductDiscount.objects.get(prodname=request.data['prodname'])
        discount_products.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def bestseller_products(request):
    product_count=[]
    #details=[]
    prod_details=Product.objects.all()
    serializer=Productserializer(prod_details,many=True)
    for product in serializer.data:
        product_count.append(product['prod_count'])
    max_count=max(product_count)
    Bestseller.objects.all().delete()  #syntax to delete all the data from db
    new_item = Product.objects.filter(prod_count=int(max_count))
    serializer4=Productserializer(new_item,many=True)
    #print(serializer4.data[0]['pcode'])
    for items in serializer4.data:
        item = Bestseller(pcode=items['pcode'], pname=items['pname'], price=items['price'], mfd=items['mfd'], exp=items['exp'], prod_count=items['prod_count'])
        item.save()
    return Response(serializer4.data)
    # for product in serializer.data:
    #     if product['prod_count']==max_count:
    #         details.append(product)
    # else:
    #     return Response(serializer4.data)

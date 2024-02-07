from django.urls import path
from.import views

urlpatterns = [
    path('product',views.Product_data),
    path('product/<int:id>',views.Product_details),
    path('discount',views.product_discount),
    path('bestseller',views.bestseller_products)
]
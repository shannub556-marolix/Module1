from django.urls import path
from .views import *
app_name='myapp'

urlpatterns = [
    path('register/',register,name='register'),
    path('home/',home,name='home'),
    path('logout/',logout_view,name='logout'),
    path('login/',login_view,name='login'),
    # path('shop/',shop,name='shop'),
    path('about/',about,name='about'),
    # path('mens/',mens,name='mens'),
    # path('women/',women,name='women'),
    path('product/',product_list, name='product_list'),
	# path('/home',home, name='home'),
	path('cart/',view_cart, name='view_cart'),
	path('add/<int:product_id>/',add_to_cart, name='add_to_cart'),
	path('remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('address/',address,name='address'),
    path('blog',blog,name='blog')
    

]





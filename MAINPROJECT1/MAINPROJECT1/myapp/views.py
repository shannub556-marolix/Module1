from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib import messages
from .forms import *

from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate,login,logout
from .models import Product, CartItem,address


# Create your views here.


def register(request):
    if request.method=="POST":
            user=User.objects.filter(username=request.POST['username'])
            if user.exists():
                  messages.info(request,'User Laready exist')
                  return redirect(reverse('myapp:register'))

            form=RegistrationForm(request.POST)
            if form.is_valid():
                  form.save()
                  return redirect(reverse('myapp:login'))
    f=RegistrationForm()
    return render(request,'register.html',context={'form':f})

def login_view(request):
    if request.method=='POST':
            form=LoginForm(request.POST)
            if form.is_valid():
                user=authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password'])
                if user:
                      login(request,user)
                      return redirect(reverse('myapp:home'))
                else:
                      messages.error(request,'Invalid username or password')
                      return redirect(reverse('myapp:login'))
    f=LoginForm()
    return render(request,'login.html',context={'form':f})


@login_required(login_url='myapp:login')
def home(request):
      return render(request,'home.html')

def logout_view(request):
      logout(request)
      return redirect(reverse('myapp:login'))

# def shop(request):
#       return render(request,'shop.html')

def about(request):
      return render(request,'about.html')

# def mens(request):
#       return render(request,'mens.html')

# def women(request):
#       return render(request,'women.html')




def product_list(request):
	products = Product.objects.all()
	return render(request, 'index.html', {'products': products})

def view_cart(request):
	cart_items = CartItem.objects.filter(user=request.user)
	total_price = sum(item.product.price * item.quantity for item in cart_items)
	return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
	product = Product.objects.get(id=product_id)
	cart_item, created = CartItem.objects.get_or_create(product=product, 
													user=request.user)
	cart_item.quantity += 1
	cart_item.save()
	return redirect('myapp:view_cart')

def remove_from_cart(request, item_id):
	cart_item = CartItem.objects.get(id=item_id)
	cart_item.delete()
	return redirect('myapp:view_cart')


def address(request):
    if request.method=='POST':
        form=addressform(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            phone_number=form.cleaned_data['phone_number']
            pincode=form.cleaned_data['pincode']
            state=form.cleaned_data['state']
            city=form.cleaned_data['city']
            colony=form.cleaned_data['colony']
            street=form.cleaned_data['street']
            address.objects.create(name='name',phone_number='phone_number',pincode='pincode',state='state',city='city',colony='colony',street='street')
    
    f1=addressform()
    return render(request,'address.html',context={'form':f1})
def blog(request):
      return render(request,'blog.html')
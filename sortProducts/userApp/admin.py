from django.contrib import admin

# Register your models here.
from .models import Product,Feedback

admin.site.register(Product)
admin.site.register(Feedback)
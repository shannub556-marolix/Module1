from django.contrib import admin
from.models import Product,ProductDiscount,Bestseller

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['pcode','pname','original_price','discount_per','mfd','exp']
admin.site.register(Product,ProductAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ['prodname','pdiscount']
admin.site.register(ProductDiscount,DiscountAdmin)

class BestsellerAdmin(admin.ModelAdmin):
    list_display = ['pcode','pname','price','mfd','exp','prod_count']
admin.site.register(Bestseller,BestsellerAdmin)


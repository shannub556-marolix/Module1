from django.contrib import admin
from .models import Module,User_data

class Useradmin(admin.ModelAdmin):
    list_display=['username','email','count']

admin.site.register(User_data,Useradmin)
admin.site.register(Module)

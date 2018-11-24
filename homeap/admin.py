from django.contrib import admin

# Register your models here.

#registering users collecions in order to insert data in it
from .models import *
admin.site.register(Users)

from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'role']


@admin.register(ProductCategory)
class ProductCategories(admin.ModelAdmin):
    pass

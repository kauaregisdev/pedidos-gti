from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'price', 'id']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['id']

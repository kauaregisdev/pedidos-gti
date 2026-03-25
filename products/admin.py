from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'id']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['id']

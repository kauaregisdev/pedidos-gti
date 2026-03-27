from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['id', 'product', 'quantity', 'unit_price', 'subtotal']

    def subtotal(self, obj):
        return obj.subtotal()

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__name', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['id', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['id']

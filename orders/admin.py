from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['id', 'product', 'quantity', 'unit_price', 'subtotal']

    def subtotal(self, obj):
        return obj.subtotal()

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['user__name', 'user__email']
    ordering = ['-created_at']
    readonly_fields = ['id', 'user', 'total', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    def get_fields(self, request, obj=None):
        return ['id', 'user', 'total', 'status', 'created_at', 'updated_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    search_fields = ['order__id', 'product__name']
    readonly_fields = ['id', 'order', 'product', 'quantity', 'unit_price']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

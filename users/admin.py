from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'name', 'is_staff', 'is_active']
    readonly_fields = ['id', 'email', 'name', 'is_active', 'is_staff', 'is_superuser', 'created_at']
    fieldsets = (
        (None, {'fields': ('id', 'email', 'name')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Datas', {'fields': ('created_at',)}),
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

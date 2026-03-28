from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Business

@admin.register(Business)
class BusinessAdmin(ModelAdmin):
    list_display = ['name', 'email', 'phone', 'founded_at']

    def has_add_permission(self, request):
        return not Business.objects.exists()

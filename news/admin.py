from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import News

@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title']
    ordering = ['-created_at']
    readonly_fields = ['title', 'description', 'created_at']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

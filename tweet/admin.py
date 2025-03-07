from django.contrib import admin

# Register your models here.
from .models import Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'photo', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['text']
    list_per_page = 10
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Tweet Information', {'fields': ['user', 'text', 'photo']}),
        ('Date Information', {'fields': ['created_at', 'updated_at']})
    ]
    class Meta:
        model = Tweet
        

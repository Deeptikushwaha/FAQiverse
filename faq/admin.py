from django.contrib import admin

# Register your models here.    #admin configuration
from .models import FAQ

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at', 'updated_at')
    search_fields = ('question', 'answer')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('question', 'answer')
        }),
        ('Translation Data', {
            'fields': ('translations',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

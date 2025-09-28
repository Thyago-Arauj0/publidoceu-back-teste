from django.contrib import admin
from .models import Checklist

@admin.register(Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'board',
        'title',
        'is_check',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'is_check',
        'created_at',
        'updated_at',
        'board',
    )

    search_fields = (
        'title',
        'board__customer__name',
    )

    ordering = ('-created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'

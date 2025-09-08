from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
        'title',
        'is_read',
        'timestamp',
        'created_at',
        'updated_at',
    )
    list_filter = ('is_read', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

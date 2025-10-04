from django.contrib import admin

from .models import FileCard
@admin.register(FileCard)
class FileCardAdminModel(admin.ModelAdmin):

    list_display = (

        'card', 'file', 'is_approved'

    )

    list_filter = (

        'card', 'is_approved'

    )
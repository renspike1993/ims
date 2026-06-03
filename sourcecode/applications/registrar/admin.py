from django.contrib import admin
from .models import Folder


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):

    list_display = (
        "folder_name",
        "floor",
        "is_active",
    )

    list_filter = (
        "floor",
        "is_active",
    )

    search_fields = (
        "folder_name",
    )

    ordering = ("folder_name",)

    # ✅ ORGANIZED INPUT FIELDS
    fieldsets = (
        ("📁 Folder Information", {
            "fields": (
                "folder_name",
                "capacity",
                "floor",
            )
        }),

        ("⚙️ Status", {
            "fields": (
                "is_active",
            )
        }),
    )
from django.contrib import admin
from .models import Folder, StudentDocument


# ======================================================
# INLINE STUDENT DOCUMENTS INSIDE FOLDER
# ======================================================
class StudentDocumentInline(admin.TabularInline):
    model = StudentDocument
    extra = 0
    fields = (
        "last_name",
        "first_name",
        "middle_name",
    )
    show_change_link = True


# ======================================================
# FOLDER ADMIN (FIXED + COMBINED)
# ======================================================
@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):

    list_display = (
        "folder_name",
        "floor",
        "capacity",
        "is_active",
        "student_count",
    )

    list_filter = (
        "floor",
        "is_active",
    )

    search_fields = (
        "folder_name",
    )

    ordering = ("folder_name",)

    inlines = [StudentDocumentInline]

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

    def student_count(self, obj):
        return obj.documents.count()
    list_per_page = 20
    student_count.short_description = "Total Students"


# ======================================================
# STUDENT DOCUMENT ADMIN
# ======================================================
@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "last_name",
        "first_name",
        "middle_name",
        "folder",
        "created_at",
    )

    # ✅ INLINE EDITABLE FIELD
    list_editable = (
        "folder",
    )


    search_fields = (
        "first_name",
        "last_name",
        "middle_name",
        "folder__folder_name",
    )

    # ✅ MAKES DROPDOWN SEARCHABLE (VERY IMPORTANT)
    autocomplete_fields = ("folder",)

    ordering = ("folder",)

    fieldsets = (
        ("📁 Folder Assignment", {
            "fields": ("folder",)
        }),

        ("👤 Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "middle_name",
            )
        }),

        ("📅 System Info", {
            "fields": ("created_at",)
        }),
    )

    readonly_fields = ("created_at",)
    list_per_page = 20
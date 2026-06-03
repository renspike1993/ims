from django.contrib import admin
from .models import Template, StudentIdentificationCard


# ======================================================
# INLINE STUDENTS UNDER TEMPLATE
# ======================================================
class StudentInline(admin.TabularInline):
    model = StudentIdentificationCard
    extra = 0
    fields = (
        "id_number",
        "first_name",
        "last_name",
        "program",
        "mobile_number",
    )
    show_change_link = True


# ======================================================
# TEMPLATE ADMIN
# ======================================================
from django.utils.html import format_html


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):

    list_display = (
        "academic_year",
        "date_started",
        "valid_until",
        "front_preview",
        "back_preview",
        "student_count",
    )

    search_fields = ("academic_year",)

    inlines = [StudentInline]

    def student_count(self, obj):
        return obj.students.count()

    student_count.short_description = "Total Students"

    def front_preview(self, obj):
        if obj.front_template:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:4px;" />',
                obj.front_template.url
            )
        return "-"

    front_preview.short_description = "Front"

    def back_preview(self, obj):
        if obj.back_template:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:4px;" />',
                obj.back_template.url
            )
        return "-"

    back_preview.short_description = "Back"


# ======================================================
# STUDENT ID ADMIN
# ======================================================
from django.contrib import admin
from .models import StudentIdentificationCard


@admin.register(StudentIdentificationCard)
class StudentIdentificationCardAdmin(admin.ModelAdmin):

    list_display = (
        "id_number",
        "template",
        "full_name_display",
        "program",
        "mobile_number",
        "guardian",
        "profile_preview",
    )

    list_filter = (
        "template",
    )

    search_fields = (
        "id_number",
        "first_name",
        "last_name",
        "guardian",
    )

    fieldsets = (

        ("📄 Template Information", {
            "fields": (
                "template",
                "id_number",

            )
        }),

        ("👨‍🎓 Student Information", {
            "fields": (
                "first_name",
                "last_name",
                "program",
            )
        }),

        ("📞 Contact Information", {
            "fields": (
                "mobile_number",
                "guardian",
                "guardian_mobile_number",
            )
        }),

        ("🖼 Profile Picture", {
            "fields": (
                "profile_picture",
            )
        }),

    )

    # =========================
    # FULL NAME DISPLAY
    # =========================
    def full_name_display(self, obj):
        return f"{obj.last_name}, {obj.first_name}"

    full_name_display.short_description = "Full Name"

    # =========================
    # PROFILE PREVIEW
    # =========================
    def profile_preview(self, obj):
        if obj.profile_picture:
            return "Yes"
        return "No"

    profile_preview.short_description = "Photo"
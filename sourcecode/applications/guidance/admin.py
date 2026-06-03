from django.contrib import admin
from .models import Exam,ExamCategory,ExamQuestion,Examinee,ExamResponse
# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse

admin.site.site_header = "Institution Management System (MOIST Inc.)"
admin.site.site_title = "Administrator"
admin.site.index_title = "Welcome"

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("exam_name", "description","duration", "created_at")





@admin.register(ExamCategory)
class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "description", "created_at")




@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ("id","exam_name","category_name","question", "correct_option")



@admin.register(Examinee)
class ExamineeAdmin(admin.ModelAdmin):
    list_display = (
        "or_number",
        "masked_full_name",
        "program",
        "exam_taken",
        "score",
        "print_result_link",
    )

    search_fields = (
        "or_number",
        "last_name",
        "first_name",
    )

    def score(self, obj):
        return ExamResponse.objects.filter(
            examinee=obj,
            is_correct=True
        ).count()

    score.short_description = "Score"

    def print_result_link(self, obj):
        url = reverse(
            "print_exam_result",
            args=[obj.id]
        )

        return format_html(
            '<a class="button" href="{}" target="_blank">Print Result</a>',
            url
        )

    print_result_link.short_description = "Result"


@admin.register(ExamResponse)
class ExamResponseAdmin(admin.ModelAdmin):
    list_display = ("examinee_question","examinee_id","is_correct","examinee_response")


    # "option_a","option_b","option_c","option_d","option_e",
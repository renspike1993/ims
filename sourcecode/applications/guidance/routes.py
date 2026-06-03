from django.urls import path
from . import views

urlpatterns = [
    path("", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("submit/", views.submit_answers, name="submit_answers"),
    path("result/", views.exam_result, name="exam_result"),
    path(
        "result/print/<int:examinee_id>/",
        views.print_exam_result,
        name="print_exam_result"
    ),
]
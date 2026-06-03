from django.urls import path
from . import views

urlpatterns = [
    path("read-csv/", views.read_csv, name="read_csv"),
]
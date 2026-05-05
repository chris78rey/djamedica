from django.urls import path

from .views import list_doctors, summary_doctors

app_name = "doctors"

urlpatterns = [
    path("", list_doctors, name="list"),
    path("summary/", summary_doctors, name="summary"),
]

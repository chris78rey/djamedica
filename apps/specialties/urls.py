from django.urls import path

from .views import list_specialties, summary_specialties

app_name = "specialties"

urlpatterns = [
    path("", list_specialties, name="list"),
    path("summary/", summary_specialties, name="summary"),
]

from django.urls import path

from .views import list_patients, summary_patients

app_name = "patients"

urlpatterns = [
    path("", list_patients, name="list"),
    path("summary/", summary_patients, name="summary"),
]

from django.urls import path

from .views import list_appointments, summary_appointments

app_name = "appointments"

urlpatterns = [
    path("", list_appointments, name="list"),
    path("summary/", summary_appointments, name="summary"),
]

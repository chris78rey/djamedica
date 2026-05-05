from django.urls import path

from .views import (
    PatientCreateView,
    PatientDeleteView,
    PatientDetailView,
    PatientManageListView,
    PatientUpdateView,
    list_patients,
    summary_patients,
)

app_name = "patients"

urlpatterns = [
    path("", list_patients, name="list"),
    path("summary/", summary_patients, name="summary"),
    path("manage/", PatientManageListView.as_view(), name="manage_list"),
    path("manage/new/", PatientCreateView.as_view(), name="create"),
    path("manage/<int:pk>/", PatientDetailView.as_view(), name="detail"),
    path("manage/<int:pk>/edit/", PatientUpdateView.as_view(), name="edit"),
    path("manage/<int:pk>/delete/", PatientDeleteView.as_view(), name="delete"),
]

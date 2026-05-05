from django.urls import path

from .views import (
    DoctorCreateView,
    DoctorDeleteView,
    DoctorDetailView,
    DoctorManageListView,
    DoctorUpdateView,
    list_doctors,
    summary_doctors,
)

app_name = "doctors"

urlpatterns = [
    path("", list_doctors, name="list"),
    path("summary/", summary_doctors, name="summary"),
    path("manage/", DoctorManageListView.as_view(), name="manage_list"),
    path("manage/new/", DoctorCreateView.as_view(), name="create"),
    path("manage/<int:pk>/", DoctorDetailView.as_view(), name="detail"),
    path("manage/<int:pk>/edit/", DoctorUpdateView.as_view(), name="edit"),
    path("manage/<int:pk>/delete/", DoctorDeleteView.as_view(), name="delete"),
]

from django.urls import path

from .views import (
    SpecialtyCreateView,
    SpecialtyDeleteView,
    SpecialtyManageListView,
    SpecialtyUpdateView,
    list_specialties,
    summary_specialties,
)

app_name = "specialties"

urlpatterns = [
    path("", list_specialties, name="list"),
    path("summary/", summary_specialties, name="summary"),
    path("manage/", SpecialtyManageListView.as_view(), name="manage_list"),
    path("manage/new/", SpecialtyCreateView.as_view(), name="create"),
    path("manage/<int:pk>/edit/", SpecialtyUpdateView.as_view(), name="edit"),
    path("manage/<int:pk>/delete/", SpecialtyDeleteView.as_view(), name="delete"),
]

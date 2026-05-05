from django.urls import path

from .views import (
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentDetailView,
    AppointmentManageListView,
    AppointmentUpdateView,
    list_appointments,
    summary_appointments,
)

app_name = "appointments"

urlpatterns = [
    path("", list_appointments, name="list"),
    path("summary/", summary_appointments, name="summary"),
    path("manage/", AppointmentManageListView.as_view(), name="manage_list"),
    path("manage/new/", AppointmentCreateView.as_view(), name="create"),
    path("manage/<int:pk>/", AppointmentDetailView.as_view(), name="detail"),
    path("manage/<int:pk>/edit/", AppointmentUpdateView.as_view(), name="edit"),
    path("manage/<int:pk>/delete/", AppointmentDeleteView.as_view(), name="delete"),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("users/", include("apps.users.urls")),
    path("specialties/", include("apps.specialties.urls")),
    path("patients/", include("apps.patients.urls")),
    path("doctors/", include("apps.doctors.urls")),
    path("appointments/", include("apps.appointments.urls")),
]

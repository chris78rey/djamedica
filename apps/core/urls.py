from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    dashboard,
    health,
    home,
    panel,
    register_choice,
    register_doctor,
    register_patient,
)

urlpatterns = [
    path("", home, name="home"),
    path("health/", health, name="health"),
    path("dashboard/", dashboard, name="dashboard"),
    path("panel/", panel, name="panel"),

    path("auth/register/", register_choice, name="register_choice"),
    path("auth/register/patient/", register_patient, name="register_patient"),
    path("auth/register/doctor/", register_doctor, name="register_doctor"),

    path(
        "auth/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
]

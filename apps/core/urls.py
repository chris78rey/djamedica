from django.contrib.auth import views as auth_views
from django.urls import path

from .views import dashboard, health, home, panel

urlpatterns = [
    path("", home, name="home"),
    path("health/", health, name="health"),
    path("dashboard/", dashboard, name="dashboard"),
    path("panel/", panel, name="panel"),
    path(
        "auth/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="logout"),
]

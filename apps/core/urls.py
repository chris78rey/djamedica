from django.urls import path

from .views import dashboard, health, home

urlpatterns = [
    path("", home, name="home"),
    path("health/", health, name="health"),
    path("dashboard/", dashboard, name="dashboard"),
]

from django.urls import path

from .views import list_users, summary_users

app_name = "users"

urlpatterns = [
    path("", list_users, name="list"),
    path("summary/", summary_users, name="summary"),
]

from django.urls import path

from .views import (
    UserCreateView,
    UserDeleteView,
    UserManageListView,
    UserUpdateView,
    list_users,
    summary_users,
)

app_name = "users"

urlpatterns = [
    path("", list_users, name="list"),
    path("summary/", summary_users, name="summary"),
    path("manage/", UserManageListView.as_view(), name="manage_list"),
    path("manage/new/", UserCreateView.as_view(), name="create"),
    path("manage/<int:pk>/edit/", UserUpdateView.as_view(), name="edit"),
    path("manage/<int:pk>/delete/", UserDeleteView.as_view(), name="delete"),
]

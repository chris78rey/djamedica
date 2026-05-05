from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import AdminRequiredMixin
from .forms import UserCreateForm, UserUpdateForm
from .models import User


def list_users(request):
    items = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.get_full_name(),
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in User.objects.order_by("id")[:20]
    ]
    return JsonResponse({"items": items})


def summary_users(request):
    return JsonResponse(
        {
            "total": User.objects.count(),
            "admins": User.objects.filter(role=User.Role.ADMIN).count(),
            "doctors": User.objects.filter(role=User.Role.DOCTOR).count(),
            "staff": User.objects.filter(role=User.Role.STAFF).count(),
            "active": User.objects.filter(is_active=True).count(),
        }
    )


class UserManageListView(AdminRequiredMixin, ListView):
    model = User
    template_name = "users/list.html"
    context_object_name = "items"
    queryset = User.objects.order_by("id")


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "common/form.html"
    success_url = reverse_lazy("users:manage_list")
    extra_context = {
        "page_title": "Crear usuario",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("users:manage_list"),
    }


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "common/form.html"
    success_url = reverse_lazy("users:manage_list")
    extra_context = {
        "page_title": "Editar usuario",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("users:manage_list"),
    }


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("users:manage_list")
    extra_context = {
        "page_title": "Eliminar usuario",
        "cancel_url": reverse_lazy("users:manage_list"),
    }

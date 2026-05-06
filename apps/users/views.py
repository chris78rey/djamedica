from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.core.mixins import AdminRequiredMixin, AuditCreateMixin, AuditUpdateMixin, DeleteSuccessMessageMixin
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
    paginate_by = 10

    def get_queryset(self):
        qs = User.objects.order_by("id")

        q = self.request.GET.get("q", "").strip()
        role = self.request.GET.get("role", "").strip()
        is_active = self.request.GET.get("is_active", "").strip()

        if q:
            qs = qs.filter(
                Q(username__icontains=q)
                | Q(email__icontains=q)
                | Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
            )

        if role in {choice[0] for choice in User.Role.choices}:
            qs = qs.filter(role=role)

        if is_active in {"1", "0"}:
            qs = qs.filter(is_active=(is_active == "1"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_q"] = self.request.GET.get("q", "").strip()
        context["filter_role"] = self.request.GET.get("role", "").strip()
        context["filter_is_active"] = self.request.GET.get("is_active", "").strip()
        context["role_choices"] = User.Role.choices
        return context


class UserDetailView(AdminRequiredMixin, DetailView):
    model = User
    template_name = "users/detail.html"
    context_object_name = "item"


class UserCreateView(AdminRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "common/form.html"
    success_url = reverse_lazy("users:manage_list")
    success_message = "Usuario creado correctamente."
    extra_context = {
        "page_title": "Crear usuario",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("users:manage_list"),
    }


class UserUpdateView(AdminRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "common/form.html"
    success_url = reverse_lazy("users:manage_list")
    success_message = "Usuario actualizado correctamente."
    extra_context = {
        "page_title": "Editar usuario",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("users:manage_list"),
    }


class UserDeleteView(AdminRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = User
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("users:manage_list")
    success_message = "Usuario eliminado correctamente."
    extra_context = {
        "page_title": "Eliminar usuario",
        "cancel_url": reverse_lazy("users:manage_list"),
    }

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import AdminRequiredMixin
from .forms import SpecialtyForm
from .models import Specialty


def list_specialties(request):
    items = [
        {
            "id": specialty.id,
            "name": specialty.name,
            "description": specialty.description,
            "is_active": specialty.is_active,
        }
        for specialty in Specialty.objects.order_by("name")[:20]
    ]
    return JsonResponse({"items": items})


def summary_specialties(request):
    return JsonResponse(
        {
            "total": Specialty.objects.count(),
            "active": Specialty.objects.filter(is_active=True).count(),
            "inactive": Specialty.objects.filter(is_active=False).count(),
        }
    )


class SpecialtyManageListView(AdminRequiredMixin, ListView):
    model = Specialty
    template_name = "specialties/list.html"
    context_object_name = "items"
    queryset = Specialty.objects.order_by("name")


class SpecialtyCreateView(AdminRequiredMixin, CreateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = "common/form.html"
    success_url = reverse_lazy("specialties:manage_list")
    extra_context = {
        "page_title": "Crear especialidad",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("specialties:manage_list"),
    }


class SpecialtyUpdateView(AdminRequiredMixin, UpdateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = "common/form.html"
    success_url = reverse_lazy("specialties:manage_list")
    extra_context = {
        "page_title": "Editar especialidad",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("specialties:manage_list"),
    }


class SpecialtyDeleteView(AdminRequiredMixin, DeleteView):
    model = Specialty
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("specialties:manage_list")
    extra_context = {
        "page_title": "Eliminar especialidad",
        "cancel_url": reverse_lazy("specialties:manage_list"),
    }

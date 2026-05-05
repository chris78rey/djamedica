from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import AdminRequiredMixin, DeleteSuccessMessageMixin
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
    paginate_by = 10

    def get_queryset(self):
        qs = Specialty.objects.order_by("name")

        q = self.request.GET.get("q", "").strip()
        is_active = self.request.GET.get("is_active", "").strip()

        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

        if is_active in {"1", "0"}:
            qs = qs.filter(is_active=(is_active == "1"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_q"] = self.request.GET.get("q", "").strip()
        context["filter_is_active"] = self.request.GET.get("is_active", "").strip()
        return context


class SpecialtyCreateView(AdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = "common/form.html"
    success_url = reverse_lazy("specialties:manage_list")
    success_message = "Especialidad creada correctamente."
    extra_context = {
        "page_title": "Crear especialidad",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("specialties:manage_list"),
    }


class SpecialtyUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Specialty
    form_class = SpecialtyForm
    template_name = "common/form.html"
    success_url = reverse_lazy("specialties:manage_list")
    success_message = "Especialidad actualizada correctamente."
    extra_context = {
        "page_title": "Editar especialidad",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("specialties:manage_list"),
    }


class SpecialtyDeleteView(AdminRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Specialty
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("specialties:manage_list")
    success_message = "Especialidad eliminada correctamente."
    extra_context = {
        "page_title": "Eliminar especialidad",
        "cancel_url": reverse_lazy("specialties:manage_list"),
    }

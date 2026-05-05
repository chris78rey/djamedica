from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import AdminRequiredMixin, ClinicalAccessRequiredMixin
from .forms import DoctorForm
from .models import Doctor


def list_doctors(request):
    items = [
        {
            "id": doctor.id,
            "full_name": doctor.user.get_full_name() or doctor.user.username,
            "email": doctor.user.email,
            "specialty": doctor.specialty.name,
            "professional_license": doctor.professional_license,
            "phone": doctor.phone,
            "office": doctor.office,
            "is_available": doctor.is_available,
        }
        for doctor in Doctor.objects.select_related("user", "specialty").order_by(
            "user__last_name", "user__first_name"
        )[:20]
    ]
    return JsonResponse({"items": items})


def summary_doctors(request):
    return JsonResponse(
        {
            "total": Doctor.objects.count(),
            "available": Doctor.objects.filter(is_available=True).count(),
            "unavailable": Doctor.objects.filter(is_available=False).count(),
        }
    )


class DoctorManageListView(ClinicalAccessRequiredMixin, ListView):
    model = Doctor
    template_name = "doctors/list.html"
    context_object_name = "items"
    queryset = Doctor.objects.select_related("user", "specialty").order_by(
        "user__last_name", "user__first_name"
    )


class DoctorCreateView(AdminRequiredMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "common/form.html"
    success_url = reverse_lazy("doctors:manage_list")
    extra_context = {
        "page_title": "Crear doctor",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("doctors:manage_list"),
    }


class DoctorUpdateView(AdminRequiredMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "common/form.html"
    success_url = reverse_lazy("doctors:manage_list")
    extra_context = {
        "page_title": "Editar doctor",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("doctors:manage_list"),
    }


class DoctorDeleteView(AdminRequiredMixin, DeleteView):
    model = Doctor
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("doctors:manage_list")
    extra_context = {
        "page_title": "Eliminar doctor",
        "cancel_url": reverse_lazy("doctors:manage_list"),
    }

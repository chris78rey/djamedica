from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.core.mixins import (
    AdminRequiredMixin,
    AuditCreateMixin,
    AuditUpdateMixin,
    ClinicalAccessRequiredMixin,
    DeleteSuccessMessageMixin,
)
from apps.specialties.models import Specialty
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
    paginate_by = 10

    def get_queryset(self):
        qs = Doctor.objects.select_related("user", "specialty").order_by(
            "user__last_name", "user__first_name"
        )

        q = self.request.GET.get("q", "").strip()
        specialty_id = self.request.GET.get("specialty_id", "").strip()
        is_available = self.request.GET.get("is_available", "").strip()

        if q:
            qs = qs.filter(
                Q(user__username__icontains=q)
                | Q(user__first_name__icontains=q)
                | Q(user__last_name__icontains=q)
                | Q(user__email__icontains=q)
                | Q(professional_license__icontains=q)
                | Q(phone__icontains=q)
            )

        if specialty_id.isdigit():
            qs = qs.filter(specialty_id=int(specialty_id))

        if is_available in {"1", "0"}:
            qs = qs.filter(is_available=(is_available == "1"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_q"] = self.request.GET.get("q", "").strip()
        context["filter_specialty_id"] = self.request.GET.get("specialty_id", "").strip()
        context["filter_is_available"] = self.request.GET.get("is_available", "").strip()
        context["specialty_choices"] = Specialty.objects.filter(is_active=True).order_by("name")
        return context


class DoctorDetailView(ClinicalAccessRequiredMixin, DetailView):
    model = Doctor
    template_name = "doctors/detail.html"
    context_object_name = "item"


class DoctorCreateView(AdminRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "common/form.html"
    success_url = reverse_lazy("doctors:manage_list")
    success_message = "Doctor creado correctamente."
    extra_context = {
        "page_title": "Crear doctor",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("doctors:manage_list"),
    }


class DoctorUpdateView(AdminRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "common/form.html"
    success_url = reverse_lazy("doctors:manage_list")
    success_message = "Doctor actualizado correctamente."
    extra_context = {
        "page_title": "Editar doctor",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("doctors:manage_list"),
    }


class DoctorDeleteView(AdminRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Doctor
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("doctors:manage_list")
    success_message = "Doctor eliminado correctamente."
    extra_context = {
        "page_title": "Eliminar doctor",
        "cancel_url": reverse_lazy("doctors:manage_list"),
    }

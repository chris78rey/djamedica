from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import ClinicalAccessRequiredMixin, StaffOrAdminRequiredMixin
from .forms import PatientForm
from .models import Patient


def list_patients(request):
    items = [
        {
            "id": patient.id,
            "document_type": patient.document_type,
            "document_number": patient.document_number,
            "full_name": patient.full_name,
            "phone": patient.phone,
            "email": patient.email,
            "is_active": patient.is_active,
        }
        for patient in Patient.objects.order_by("last_name", "first_name")[:20]
    ]
    return JsonResponse({"items": items})


def summary_patients(request):
    return JsonResponse(
        {
            "total": Patient.objects.count(),
            "active": Patient.objects.filter(is_active=True).count(),
            "inactive": Patient.objects.filter(is_active=False).count(),
        }
    )


class PatientManageListView(ClinicalAccessRequiredMixin, ListView):
    model = Patient
    template_name = "patients/list.html"
    context_object_name = "items"
    queryset = Patient.objects.order_by("last_name", "first_name")


class PatientCreateView(StaffOrAdminRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "common/form.html"
    success_url = reverse_lazy("patients:manage_list")
    extra_context = {
        "page_title": "Crear paciente",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("patients:manage_list"),
    }


class PatientUpdateView(StaffOrAdminRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "common/form.html"
    success_url = reverse_lazy("patients:manage_list")
    extra_context = {
        "page_title": "Editar paciente",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("patients:manage_list"),
    }


class PatientDeleteView(StaffOrAdminRequiredMixin, DeleteView):
    model = Patient
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("patients:manage_list")
    extra_context = {
        "page_title": "Eliminar paciente",
        "cancel_url": reverse_lazy("patients:manage_list"),
    }

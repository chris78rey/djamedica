from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.core.mixins import (
    AuditCreateMixin,
    AuditUpdateMixin,
    ClinicalAccessRequiredMixin,
    DeleteSuccessMessageMixin,
    StaffOrAdminRequiredMixin,
)
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
    paginate_by = 10

    def get_queryset(self):
        qs = Patient.objects.order_by("last_name", "first_name")

        q = self.request.GET.get("q", "").strip()
        document_type = self.request.GET.get("document_type", "").strip()
        is_active = self.request.GET.get("is_active", "").strip()

        if q:
            qs = qs.filter(
                Q(first_name__icontains=q)
                | Q(last_name__icontains=q)
                | Q(document_number__icontains=q)
                | Q(phone__icontains=q)
                | Q(email__icontains=q)
            )

        if document_type in {choice[0] for choice in Patient.DocumentType.choices}:
            qs = qs.filter(document_type=document_type)

        if is_active in {"1", "0"}:
            qs = qs.filter(is_active=(is_active == "1"))

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_q"] = self.request.GET.get("q", "").strip()
        context["filter_document_type"] = self.request.GET.get("document_type", "").strip()
        context["filter_is_active"] = self.request.GET.get("is_active", "").strip()
        context["document_type_choices"] = Patient.DocumentType.choices
        return context


class PatientDetailView(ClinicalAccessRequiredMixin, DetailView):
    model = Patient
    template_name = "patients/detail.html"
    context_object_name = "item"


class PatientCreateView(StaffOrAdminRequiredMixin, SuccessMessageMixin, AuditCreateMixin, CreateView):
    model = Patient
    form_class = PatientForm
    template_name = "common/form.html"
    success_url = reverse_lazy("patients:manage_list")
    success_message = "Paciente creado correctamente."
    extra_context = {
        "page_title": "Crear paciente",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("patients:manage_list"),
    }


class PatientUpdateView(StaffOrAdminRequiredMixin, SuccessMessageMixin, AuditUpdateMixin, UpdateView):
    model = Patient
    form_class = PatientForm
    template_name = "common/form.html"
    success_url = reverse_lazy("patients:manage_list")
    success_message = "Paciente actualizado correctamente."
    extra_context = {
        "page_title": "Editar paciente",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("patients:manage_list"),
    }


class PatientDeleteView(StaffOrAdminRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Patient
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("patients:manage_list")
    success_message = "Paciente eliminado correctamente."
    extra_context = {
        "page_title": "Eliminar paciente",
        "cancel_url": reverse_lazy("patients:manage_list"),
    }

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import ClinicalAccessRequiredMixin, StaffOrAdminRequiredMixin
from .forms import AppointmentForm
from .models import Appointment


def list_appointments(request):
    items = [
        {
            "id": appointment.id,
            "patient": appointment.patient.full_name,
            "doctor": appointment.doctor.user.get_full_name() or appointment.doctor.user.username,
            "specialty": appointment.specialty.name,
            "scheduled_at": appointment.scheduled_at.isoformat(),
            "duration_minutes": appointment.duration_minutes,
            "status": appointment.status,
            "reason": appointment.reason,
        }
        for appointment in Appointment.objects.select_related(
            "patient",
            "doctor__user",
            "specialty",
        ).order_by("-scheduled_at")[:20]
    ]
    return JsonResponse({"items": items})


def summary_appointments(request):
    return JsonResponse(
        {
            "total": Appointment.objects.count(),
            "scheduled": Appointment.objects.filter(
                status=Appointment.Status.SCHEDULED
            ).count(),
            "confirmed": Appointment.objects.filter(
                status=Appointment.Status.CONFIRMED
            ).count(),
            "completed": Appointment.objects.filter(
                status=Appointment.Status.COMPLETED
            ).count(),
            "cancelled": Appointment.objects.filter(
                status=Appointment.Status.CANCELLED
            ).count(),
            "no_show": Appointment.objects.filter(
                status=Appointment.Status.NO_SHOW
            ).count(),
        }
    )


class AppointmentManageListView(ClinicalAccessRequiredMixin, ListView):
    model = Appointment
    template_name = "appointments/list.html"
    context_object_name = "items"

    def get_queryset(self):
        qs = Appointment.objects.select_related(
            "patient",
            "doctor__user",
            "specialty",
            "created_by",
        ).order_by("-scheduled_at")

        user = self.request.user
        if getattr(user, "role", None) == "DOCTOR" and not user.is_superuser:
            qs = qs.filter(doctor__user=user)

        return qs


class AppointmentCreateView(StaffOrAdminRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "common/form.html"
    success_url = reverse_lazy("appointments:manage_list")
    extra_context = {
        "page_title": "Crear cita",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("appointments:manage_list"),
    }


class AppointmentUpdateView(StaffOrAdminRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "common/form.html"
    success_url = reverse_lazy("appointments:manage_list")
    extra_context = {
        "page_title": "Editar cita",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("appointments:manage_list"),
    }


class AppointmentDeleteView(StaffOrAdminRequiredMixin, DeleteView):
    model = Appointment
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("appointments:manage_list")
    extra_context = {
        "page_title": "Eliminar cita",
        "cancel_url": reverse_lazy("appointments:manage_list"),
    }

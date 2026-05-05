from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.core.mixins import (
    ClinicalAccessRequiredMixin,
    DeleteSuccessMessageMixin,
    StaffOrAdminRequiredMixin,
)
from apps.doctors.models import Doctor
from apps.specialties.models import Specialty
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
    paginate_by = 10

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

        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        doctor_id = self.request.GET.get("doctor_id", "").strip()
        specialty_id = self.request.GET.get("specialty_id", "").strip()
        date_from = self.request.GET.get("date_from", "").strip()
        date_to = self.request.GET.get("date_to", "").strip()

        if q:
            qs = qs.filter(
                Q(patient__first_name__icontains=q)
                | Q(patient__last_name__icontains=q)
                | Q(patient__document_number__icontains=q)
                | Q(doctor__user__first_name__icontains=q)
                | Q(doctor__user__last_name__icontains=q)
                | Q(reason__icontains=q)
            )

        if status in {choice[0] for choice in Appointment.Status.choices}:
            qs = qs.filter(status=status)

        if doctor_id.isdigit():
            qs = qs.filter(doctor_id=int(doctor_id))

        if specialty_id.isdigit():
            qs = qs.filter(specialty_id=int(specialty_id))

        if date_from:
            qs = qs.filter(scheduled_at__date__gte=date_from)

        if date_to:
            qs = qs.filter(scheduled_at__date__lte=date_to)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_q"] = self.request.GET.get("q", "").strip()
        context["filter_status"] = self.request.GET.get("status", "").strip()
        context["filter_doctor_id"] = self.request.GET.get("doctor_id", "").strip()
        context["filter_specialty_id"] = self.request.GET.get("specialty_id", "").strip()
        context["filter_date_from"] = self.request.GET.get("date_from", "").strip()
        context["filter_date_to"] = self.request.GET.get("date_to", "").strip()
        context["status_choices"] = Appointment.Status.choices
        context["doctor_choices"] = Doctor.objects.select_related("user").order_by(
            "user__last_name", "user__first_name"
        )
        context["specialty_choices"] = Specialty.objects.filter(is_active=True).order_by("name")
        return context


class AppointmentDetailView(ClinicalAccessRequiredMixin, DetailView):
    model = Appointment
    template_name = "appointments/detail.html"
    context_object_name = "item"

    def get_queryset(self):
        qs = Appointment.objects.select_related(
            "patient",
            "doctor__user",
            "specialty",
            "created_by",
        )
        user = self.request.user
        if getattr(user, "role", None) == "DOCTOR" and not user.is_superuser:
            qs = qs.filter(doctor__user=user)
        return qs


class AppointmentCreateView(StaffOrAdminRequiredMixin, SuccessMessageMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "common/form.html"
    success_url = reverse_lazy("appointments:manage_list")
    success_message = "Cita creada correctamente."
    extra_context = {
        "page_title": "Crear cita",
        "submit_label": "Guardar",
        "cancel_url": reverse_lazy("appointments:manage_list"),
    }

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AppointmentUpdateView(StaffOrAdminRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "common/form.html"
    success_url = reverse_lazy("appointments:manage_list")
    success_message = "Cita actualizada correctamente."
    extra_context = {
        "page_title": "Editar cita",
        "submit_label": "Actualizar",
        "cancel_url": reverse_lazy("appointments:manage_list"),
    }


class AppointmentDeleteView(StaffOrAdminRequiredMixin, DeleteSuccessMessageMixin, DeleteView):
    model = Appointment
    template_name = "common/confirm_delete.html"
    success_url = reverse_lazy("appointments:manage_list")
    success_message = "Cita eliminada correctamente."
    extra_context = {
        "page_title": "Eliminar cita",
        "cancel_url": reverse_lazy("appointments:manage_list"),
    }

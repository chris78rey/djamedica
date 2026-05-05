from django.http import JsonResponse

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

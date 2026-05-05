from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor
from apps.patients.models import Patient
from apps.specialties.models import Specialty
from apps.users.models import User


def home(request):
    return render(request, "core/home.html", {"project_name": "Djamedica"})


def health(request):
    return JsonResponse(
        {"status": "ok", "app": "djamedica", "framework": "django"}
    )


def dashboard(request):
    return JsonResponse(
        {
            "users": User.objects.count(),
            "specialties": Specialty.objects.count(),
            "patients": Patient.objects.count(),
            "doctors": Doctor.objects.count(),
            "appointments": Appointment.objects.count(),
        }
    )


@login_required
def panel(request):
    user = request.user
    today = timezone.localdate()
    next_7 = today + timezone.timedelta(days=7)
    now = timezone.now()

    appointments_qs = Appointment.objects.select_related(
        "patient",
        "doctor__user",
        "specialty",
    )

    if getattr(user, "role", None) == "DOCTOR" and not user.is_superuser:
        appointments_qs = appointments_qs.filter(doctor__user=user)

    metrics = appointments_qs.aggregate(
        total=Count("id"),
        scheduled=Count("id", filter=Q(status=Appointment.Status.SCHEDULED)),
        confirmed=Count("id", filter=Q(status=Appointment.Status.CONFIRMED)),
        completed=Count("id", filter=Q(status=Appointment.Status.COMPLETED)),
        cancelled=Count("id", filter=Q(status=Appointment.Status.CANCELLED)),
        no_show=Count("id", filter=Q(status=Appointment.Status.NO_SHOW)),
        today_total=Count("id", filter=Q(scheduled_at__date=today)),
        next_7_days=Count("id", filter=Q(scheduled_at__date__gte=today, scheduled_at__date__lte=next_7)),
    )

    upcoming = appointments_qs.filter(
        scheduled_at__gte=now,
        status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED],
    ).order_by("scheduled_at")[:8]

    recent_completed = appointments_qs.filter(
        status=Appointment.Status.COMPLETED
    ).order_by("-scheduled_at")[:5]

    specialty_stats = list(
        appointments_qs.values("specialty__name")
        .annotate(total=Count("id"))
        .order_by("-total", "specialty__name")[:5]
    )

    context = {
        "project_name": "Djamedica",
        "users_count": User.objects.count(),
        "specialties_count": Specialty.objects.count(),
        "patients_count": Patient.objects.filter(is_active=True).count(),
        "doctors_count": Doctor.objects.filter(is_available=True).count(),
        "appointments_total": metrics["total"] or 0,
        "appointments_scheduled": metrics["scheduled"] or 0,
        "appointments_confirmed": metrics["confirmed"] or 0,
        "appointments_completed": metrics["completed"] or 0,
        "appointments_cancelled": metrics["cancelled"] or 0,
        "appointments_no_show": metrics["no_show"] or 0,
        "appointments_today": metrics["today_total"] or 0,
        "appointments_next_7_days": metrics["next_7_days"] or 0,
        "upcoming_appointments": upcoming,
        "recent_completed_appointments": recent_completed,
        "specialty_stats": specialty_stats,
    }
    return render(request, "core/panel.html", context)

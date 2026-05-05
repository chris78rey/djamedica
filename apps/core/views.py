from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

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

    appointments_qs = Appointment.objects.all()
    if getattr(user, "role", None) == "DOCTOR" and not user.is_superuser:
        appointments_qs = appointments_qs.filter(doctor__user=user)

    context = {
        "project_name": "Djamedica",
        "users_count": User.objects.count(),
        "specialties_count": Specialty.objects.count(),
        "patients_count": Patient.objects.count(),
        "doctors_count": Doctor.objects.count(),
        "appointments_count": appointments_qs.count(),
    }
    return render(request, "core/panel.html", context)

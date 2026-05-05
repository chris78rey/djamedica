from django.http import JsonResponse

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

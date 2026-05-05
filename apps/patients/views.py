from django.http import JsonResponse

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

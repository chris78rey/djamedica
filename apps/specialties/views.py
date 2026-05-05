from django.http import JsonResponse

from .models import Specialty


def list_specialties(request):
    items = [
        {
            "id": specialty.id,
            "name": specialty.name,
            "description": specialty.description,
            "is_active": specialty.is_active,
        }
        for specialty in Specialty.objects.order_by("name")[:20]
    ]
    return JsonResponse({"items": items})


def summary_specialties(request):
    return JsonResponse(
        {
            "total": Specialty.objects.count(),
            "active": Specialty.objects.filter(is_active=True).count(),
            "inactive": Specialty.objects.filter(is_active=False).count(),
        }
    )

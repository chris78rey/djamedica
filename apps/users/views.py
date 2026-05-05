from django.http import JsonResponse

from .models import User


def list_users(request):
    items = [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.get_full_name(),
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in User.objects.order_by("id")[:20]
    ]
    return JsonResponse({"items": items})


def summary_users(request):
    return JsonResponse(
        {
            "total": User.objects.count(),
            "admins": User.objects.filter(role=User.Role.ADMIN).count(),
            "doctors": User.objects.filter(role=User.Role.DOCTOR).count(),
            "staff": User.objects.filter(role=User.Role.STAFF).count(),
            "active": User.objects.filter(is_active=True).count(),
        }
    )

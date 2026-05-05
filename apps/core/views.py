from django.http import JsonResponse
from django.shortcuts import render


def home(request):
    return render(request, "base.html", {"project_name": "Djamedica"})


def health(request):
    return JsonResponse({"status": "ok", "app": "djamedica", "framework": "django"})

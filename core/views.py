import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.services.ingestion import IngestionService
from core.services.resolution import EntityResolutionService
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os
import platform
from django import get_version as django_version

def home(request):
    """Render the landing screen with loader and environment details."""
    host_name = request.get_host().lower()
    agent_brand = "AppWizzy" if host_name == "appwizzy.com" else "Flatlogic"
    now = timezone.now()

    context = {
        "project_name": "New Style",
        "agent_brand": agent_brand,
        "django_version": django_version(),
        "python_version": platform.python_version(),
        "current_time": now,
        "host_name": host_name,
        "project_description": os.getenv("PROJECT_DESCRIPTION", ""),
        "project_image_url": os.getenv("PROJECT_IMAGE_URL", ""),
    }
    return render(request, "core/index.html", context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('core:dashboard')
    return render(request, 'core/login.html')

@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html', {'project_name': 'New Style'})

def logout_view(request):
    logout(request)
    return redirect('core:home')

@csrf_exempt
def ingest_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Using IngestionService as a placeholder for actual processing
        result = IngestionService.ingest(data)
        return JsonResponse({'status': 'success', 'data': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def resolve_entities(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Using EntityResolutionService as a placeholder for actual processing
        result = EntityResolutionService.resolve(data)
        return JsonResponse({'status': 'success', 'result': result})
    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.shortcuts import render
from prometheus_client import generate_latest, REGISTRY, Counter, Histogram
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import time
import json
import os

# Use the default registry instead of a custom one to ensure metrics persistence
# Remove the custom registry creation since we'll use the default REGISTRY

# Use deployment name as a stable identifier
app_name = "static-webpage"

# Define metrics using default registry
page_visit_counter = Counter('page_visits_total', 'Total number of page visits',
                           ['app'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds',
                          ['method', 'endpoint', 'app'])
PAGE_LOAD_TIME = Histogram('page_load_time_seconds', 'Page load time in seconds',
                         ['app'])

def devops_page(request):
    """Render the DevOps page."""
    start_time = time()
    response = render(request, 'app/devops.html')
    page_visit_counter.labels(app=app_name).inc()
    duration = time() - start_time
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path,
        app=app_name
    ).observe(duration)
    return response

def metrics(request):
    """Expose Prometheus metrics."""
    start_time = time()
    # Use the default REGISTRY instead of custom registry
    response = HttpResponse(generate_latest(REGISTRY), content_type="text/plain; charset=utf-8")
    duration = time() - start_time
    REQUEST_LATENCY.labels(
        method=request.method,
        endpoint=request.path,
        app=app_name
    ).observe(duration)
    return response

@csrf_exempt
def track_page_load(request):
    """Track page load time from JavaScript POST requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            load_time = data.get('load_time', 0) / 1000  # Convert ms to seconds
            PAGE_LOAD_TIME.labels(app=app_name).observe(load_time)
            return JsonResponse({'status': 'success', 'message': 'Page load time recorded'})
        except (ValueError, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

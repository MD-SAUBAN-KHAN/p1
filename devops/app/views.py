from django.shortcuts import render
from prometheus_client import generate_latest, REGISTRY, Counter, Histogram
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import time
import json

# Unique application name for metric labels
app_name = "static-webpage"

# Check if metrics already exist in REGISTRY to avoid duplication
if "page_visits_total" not in REGISTRY._names_to_collectors:
    page_visit_counter = Counter('page_visits_total', 'Total number of page visits', ['app'])
    REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint', 'app'])
    PAGE_LOAD_TIME = Histogram('page_load_time_seconds', 'Page load time in seconds', ['app'])
else:
    page_visit_counter = REGISTRY._names_to_collectors["page_visits_total"]
    REQUEST_LATENCY = REGISTRY._names_to_collectors["request_latency_seconds"]
    PAGE_LOAD_TIME = REGISTRY._names_to_collectors["page_load_time_seconds"]

def devops_page(request):
    """Render the DevOps page."""
    start_time = time()
    response = render(request, 'app/devops.html')

    # Increment page visit counter
    page_visit_counter.labels(app=app_name).inc()

    # Measure request latency
    duration = time() - start_time
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path, app=app_name).observe(duration)

    return response

def metrics(request):
    """Expose Prometheus metrics."""
    response = HttpResponse(generate_latest(), content_type="text/plain; charset=utf-8")
    return response

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@csrf_exempt
def track_page_load(request):
    """Track page load time from JavaScript POST requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            load_time = data.get('load_time', 0) / 1000  # Convert ms to seconds
            logger.debug(f"Received load time: {load_time}")
            PAGE_LOAD_TIME.labels(app=app_name, pod=os.getenv("HOSTNAME", "unknown")).observe(load_time)
            return JsonResponse({'status': 'success', 'message': 'Page load time recorded'})
        except (ValueError, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

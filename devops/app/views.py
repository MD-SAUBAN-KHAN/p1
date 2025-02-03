from django.shortcuts import render
from prometheus_client import generate_latest, CollectorRegistry, Counter, Histogram
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from time import time
import json

# Create a global registry and metrics
#registry = CollectorRegistry()

# Use custom metrics
page_visit_counter = Counter('page_visits_total', 'Total number of page visits') #registry=registry)
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint']) #registry=registry)
PAGE_LOAD_TIME = Histogram('page_load_time_seconds', 'Page load time in seconds')# registry=registry)

def devops_page(request):
    """Render the DevOps page."""
    
    response = render(request, 'app/devops.html')
    

    
    page_visit_counter.inc()  # Increment counter here

    return response

def metrics(request):
    """Expose Prometheus metrics."""
    start_time = time()  # Start measuring time
    response = HttpResponse(generate_latest(), content_type="text/plain; charset=utf-8")
    duration = time() - start_time  # Calculate latency
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).observe(duration)
    #with REQUEST_LATENCY.labels(method=request.method, endpoint=request.path).time():
    #    page_visit_counter.inc()
    return response

@csrf_exempt
def track_page_load(request):
    """Track page load time from JavaScript POST requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            load_time = data.get('load_time', 0) / 1000  # Convert ms to seconds
            PAGE_LOAD_TIME.observe(load_time)
            return JsonResponse({'status': 'success', 'message': 'Page load time recorded'})
        except (ValueError, KeyError):
            return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

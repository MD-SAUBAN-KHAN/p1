"""
URL configuration for devops project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from app import views  
from django_prometheus import exports

urlpatterns = [
    path('', views.devops_page, name='devops_page'),
    path('metrics/', exports.ExportToDjangoView),  # Correctly reference views.metrics
    path('metrics/', exports.ExportToPrometheus),
]




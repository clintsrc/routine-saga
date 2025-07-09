# pylint: disable=unused-argument

"""
URL configuration for core project.

The `urlpatterns` list maps URLs (endpoints) to views (routes)
        Ref: https://docs.djangoproject.com/en/5.2/topics/http/urls/
Example methodologies:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another urls.py (this will 'build up' the full endpoint path)
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpRequest, HttpResponse, JsonResponse


def home_view(request: HttpRequest) -> HttpResponse:
    """A minimal view to verify the deployment"""
    return HttpResponse("Forthcoming! A Django Routine Saga app!")


def health_check(request: HttpRequest) -> JsonResponse:
    """A pingable keepalive route for the hosting service to call"""
    return JsonResponse({"status": "ok"})


# define all urls for the website
urlpatterns = [
    # admin endpoints
    path("admin/", admin.site.urls),
    # user account endpoints
    path("accounts/", include("accounts.urls")),
    # main app site endpoints
    path("", include("notes.urls")),
    # infrastructure-related endpoints
    path("healthz/", health_check),
]

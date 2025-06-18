"""
URL configuration for the main app (home page).
"""

from django.urls import path, include
from . import views  # import ./views.py

# Unique name helps Django to identify this specific urls.py
app_name = "notes"

# define all urls for the website
urlpatterns = [
    # Home page
    # Add "" to the route to match the default (root) path "/"
    # views.index: the function Django will call in views.py when this route is matched
    # name="index": a name/alias for this route (useful for reverse lookups)
    path("", views.index, name="index"),
    # Any additional pages available for this app...
    path("topics/", views.topics, name="topics"),
]

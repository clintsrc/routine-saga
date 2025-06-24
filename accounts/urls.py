"""
URL configuration for the accounts app (login page).
"""

from django.urls import path, include

# Unique name helps Django to identify this specific urls.py
app_name = "accounts"

# define all urls for the admin website
urlpatterns = [
    # Login page
    # Add "" to the route to match the default (root url) path "/"
    # django urls provide 'accounts/login' and 'accounts/logout' urls
    path("", include("django.contrib.auth.urls")),
    # Any additional pages available for this app...
]
